"""
Skills Ablation Study
Author: Leo Ji

Systematically test the contribution of each skill to overall performance.
"""

import re
from pathlib import Path
from typing import List, Dict, Any
from evaluation.ab_testing_evaluator import ABTestingEvaluator, ABTestConfiguration


class SkillsAblator:
    """
    Tools for conducting ablation studies on agent skills.
    
    Systematically removes skills to measure their individual contributions.
    """
    
    def __init__(self, rules_file: str = "agent_rules.md"):
        """
        Initialize skills ablator.
        
        Args:
            rules_file: Path to rules file containing skills
        """
        self.rules_file = rules_file
        self.rules_path = Path("rules") / rules_file
        
        # Load full rules
        with open(self.rules_path, 'r', encoding='utf-8') as f:
            self.full_rules = f.read()
        
        # Extract all skills
        self.skills = self._extract_all_skills()
        
        print(f"📚 Loaded {len(self.skills)} skills from {rules_file}")
        for i, skill in enumerate(self.skills, 1):
            print(f"   {i}. {skill}")
    
    def _extract_all_skills(self) -> List[str]:
        """
        Extract all skill names from rules file.
        
        Returns:
            List of skill names
        """
        # Match pattern: ## 📚 Skill: XXX
        pattern = r'## (?:📚 )?Skill: ([^\n]+)'
        matches = re.findall(pattern, self.full_rules)
        return matches
    
    def _remove_skill(self, skill_name: str, content: str) -> str:
        """
        Remove a specific skill from rules content.
        
        Args:
            skill_name: Name of skill to remove
            content: Full rules content
            
        Returns:
            Rules content with skill removed
        """
        # Find skill section
        marker = f"## 📚 Skill: {skill_name}"
        
        if marker not in content:
            # Try without emoji
            marker = f"## Skill: {skill_name}"
        
        if marker not in content:
            print(f"⚠️  Warning: Skill '{skill_name}' not found")
            return content
        
        # Find start of this skill
        start_idx = content.index(marker)
        
        # Find next skill (or end of file)
        remaining = content[start_idx:]
        next_skill = remaining.find('\n## ', 1)
        
        if next_skill != -1:
            # Remove from start to next skill
            end_idx = start_idx + next_skill
            modified = content[:start_idx] + content[end_idx:]
        else:
            # Remove from start to end of file
            modified = content[:start_idx]
        
        return modified
    
    def generate_ablation_config(
        self,
        config_name: str,
        skills_to_remove: List[str],
        description: str = ""
    ) -> str:
        """
        Generate rules content with specific skills removed.
        
        Args:
            config_name: Name for this configuration
            skills_to_remove: List of skill names to remove
            description: Description of this ablation
            
        Returns:
            Modified rules content
        """
        modified_rules = self.full_rules
        
        # Remove each skill
        for skill in skills_to_remove:
            modified_rules = self._remove_skill(skill, modified_rules)
        
        # Add ablation note at the beginning
        note = f"""
# Ablation Configuration: {config_name}
**Type:** Skills Ablation Study
**Removed Skills:** {', '.join(skills_to_remove) if skills_to_remove else 'None (Baseline)'}
**Description:** {description}

---

"""
        return note + modified_rules
    
    def create_single_skill_ablations(
        self,
        include_baseline: bool = True
    ) -> List[ABTestConfiguration]:
        """
        Create configurations removing one skill at a time.
        
        Args:
            include_baseline: Whether to include full baseline config
            
        Returns:
            List of test configurations
        """
        configs = []
        
        # Baseline (all skills)
        if include_baseline:
            baseline = ABTestConfiguration(
                name="Baseline_AllSkills",
                rules_files=["agent_rules.md", "analysis_rules.md"],
                description="Baseline: All skills included"
            )
            configs.append(baseline)
        
        # Remove one skill at a time
        for skill in self.skills:
            # Create temporary file with this skill removed
            config_name = f"Ablation_No_{skill.replace(' ', '_')}"
            
            # Generate modified rules
            modified_rules = self.generate_ablation_config(
                config_name=config_name,
                skills_to_remove=[skill],
                description=f"Remove '{skill}' skill to test its contribution"
            )
            
            # Save to temporary file
            temp_file = f"temp_ablation_{config_name}.md"
            temp_path = Path("rules") / temp_file
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(modified_rules)
            
            # Create configuration
            config = ABTestConfiguration(
                name=config_name,
                rules_files=[temp_file, "analysis_rules.md"],
                description=f"Ablation: Remove '{skill}' skill"
            )
            configs.append(config)
        
        return configs
    
    def create_cumulative_ablations(self) -> List[ABTestConfiguration]:
        """
        Create configurations removing skills cumulatively.
        
        Tests: Remove least important → most important
        
        Returns:
            List of test configurations
        """
        configs = []
        
        # Start with all skills
        remaining_skills = self.skills.copy()
        removed_skills = []
        
        # Baseline
        baseline = ABTestConfiguration(
            name="Cumulative_00_AllSkills",
            rules_files=["agent_rules.md", "analysis_rules.md"],
            description="Baseline: All skills"
        )
        configs.append(baseline)
        
        # Remove one skill at a time (cumulative)
        for i, skill in enumerate(self.skills, 1):
            removed_skills.append(skill)
            
            config_name = f"Cumulative_{i:02d}_Remove{i}Skills"
            
            # Generate modified rules
            modified_rules = self.generate_ablation_config(
                config_name=config_name,
                skills_to_remove=removed_skills,
                description=f"Removed {i} skills: {', '.join(removed_skills)}"
            )
            
            # Save to temporary file
            temp_file = f"temp_cumulative_{i:02d}.md"
            temp_path = Path("rules") / temp_file
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(modified_rules)
            
            # Create configuration
            config = ABTestConfiguration(
                name=config_name,
                rules_files=[temp_file, "analysis_rules.md"],
                description=f"Cumulative ablation: {i} skills removed"
            )
            configs.append(config)
        
        return configs
    
    def create_category_ablations(self) -> List[ABTestConfiguration]:
        """
        Create configurations removing skills by category.
        
        Categories:
        - Core Operations (Search, Export, Visualization)
        - Advanced Analysis (Analysis, Anomaly Detection)
        - Utilities (Code Execution, Knowledge Base)
        
        Returns:
            List of test configurations
        """
        configs = []
        
        # Define skill categories
        categories = {
            "CoreOperations": [
                "Options Search",
                "Data Export",
                "Visualization"
            ],
            "AdvancedAnalysis": [
                "Professional Analysis",
                "Anomaly Detection"
            ],
            "Utilities": [
                "Custom Code Execution",
                "Knowledge Base Management"
            ]
        }
        
        # Baseline
        baseline = ABTestConfiguration(
            name="Category_Baseline",
            rules_files=["agent_rules.md", "analysis_rules.md"],
            description="Baseline: All skill categories"
        )
        configs.append(baseline)
        
        # Remove each category
        for category_name, skills in categories.items():
            # Filter skills that actually exist
            skills_to_remove = [s for s in skills if s in self.skills]
            
            if not skills_to_remove:
                continue
            
            config_name = f"Category_No_{category_name}"
            
            # Generate modified rules
            modified_rules = self.generate_ablation_config(
                config_name=config_name,
                skills_to_remove=skills_to_remove,
                description=f"Remove {category_name} category"
            )
            
            # Save to temporary file
            temp_file = f"temp_category_{category_name}.md"
            temp_path = Path("rules") / temp_file
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(modified_rules)
            
            # Create configuration
            config = ABTestConfiguration(
                name=config_name,
                rules_files=[temp_file, "analysis_rules.md"],
                description=f"Category ablation: Remove {category_name}"
            )
            configs.append(config)
        
        return configs
    
    def cleanup_temp_files(self):
        """Clean up temporary ablation rule files."""
        rules_dir = Path("rules")
        temp_files = list(rules_dir.glob("temp_*.md"))
        
        for temp_file in temp_files:
            temp_file.unlink()
            print(f"🗑️  Cleaned up: {temp_file.name}")
        
        if temp_files:
            print(f"✅ Cleaned up {len(temp_files)} temporary files")


def run_skills_ablation_study(
    ablation_type: str = "single",
    test_questions: List[str] = None,
    runs_per_question: int = 3
) -> Dict[str, Any]:
    """
    Run a complete skills ablation study.
    
    Args:
        ablation_type: Type of ablation ("single", "cumulative", "category")
        test_questions: List of questions to test
        runs_per_question: Number of runs per question
        
    Returns:
        Ablation study results
    """
    # Default test questions
    if test_questions is None:
        test_questions = [
            "Get AAPL options for December 2025",
            "Analyze TSLA options sentiment for November",
            "Compare NVDA and AMD options positioning"
        ]
    
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🔬 SKILLS ABLATION STUDY                                 ║
║                                                                    ║
║  Systematically test each skill's contribution                     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    # Initialize ablator
    ablator = SkillsAblator("agent_rules.md")
    
    # Create configurations based on type
    print(f"\n📋 Creating {ablation_type} ablation configurations...")
    
    if ablation_type == "single":
        configs = ablator.create_single_skill_ablations()
        print(f"✅ Created {len(configs)} configurations (1 baseline + {len(configs)-1} ablations)")
    
    elif ablation_type == "cumulative":
        configs = ablator.create_cumulative_ablations()
        print(f"✅ Created {len(configs)} configurations (cumulative removal)")
    
    elif ablation_type == "category":
        configs = ablator.create_category_ablations()
        print(f"✅ Created {len(configs)} configurations (category-based)")
    
    else:
        raise ValueError(f"Unknown ablation type: {ablation_type}")
    
    # Initialize evaluator
    print("\n🔧 Setting up evaluator...")
    evaluator = ABTestingEvaluator()
    
    # Add all configurations
    for config in configs:
        evaluator.add_configuration(config)
    
    # Run tests
    print(f"\n{'='*70}")
    print("🧪 RUNNING ABLATION TESTS")
    print(f"{'='*70}")
    print(f"Questions: {len(test_questions)}")
    print(f"Runs per question: {runs_per_question}")
    print(f"Total runs: {len(configs) * len(test_questions) * runs_per_question}")
    print()
    
    results = evaluator.run_ab_comparison(
        questions=test_questions,
        runs_per_question=runs_per_question
    )
    
    # Analyze results
    print(f"\n{'='*70}")
    print("📊 ABLATION ANALYSIS")
    print(f"{'='*70}")
    
    analysis = analyze_skill_contributions(results, ablator.skills, ablation_type)
    
    # Print report
    evaluator.print_comparison_report(results)
    
    # Cleanup
    print(f"\n{'='*70}")
    print("🗑️  CLEANUP")
    print(f"{'='*70}")
    ablator.cleanup_temp_files()
    
    # Save results
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/skills_ablation_{ablation_type}_{timestamp}.json"
    evaluator.save_results(filename)
    
    return {
        "results": results,
        "analysis": analysis,
        "filename": filename
    }


def analyze_skill_contributions(
    results: Dict[str, Any],
    skills: List[str],
    ablation_type: str
) -> Dict[str, Any]:
    """
    Analyze skill contributions from ablation results.
    
    Args:
        results: Ablation test results
        skills: List of skill names
        ablation_type: Type of ablation performed
        
    Returns:
        Analysis of skill contributions
    """
    analysis = {
        "ablation_type": ablation_type,
        "skill_contributions": {},
        "rankings": []
    }
    
    summary = results.get("summary", {})
    
    if ablation_type == "single":
        # Get baseline score
        baseline_score = summary.get("Baseline_AllSkills", {}).get("mean_score", 0)
        baseline_robustness = summary.get("Baseline_AllSkills", {}).get("mean_robustness", 0)
        
        print(f"\n🎯 Baseline Performance:")
        print(f"   Score: {baseline_score}/10")
        print(f"   Robustness: {baseline_robustness}/10")
        print()
        
        print(f"📊 Individual Skill Contributions:")
        print()
        
        contributions = []
        
        for skill in skills:
            config_name = f"Ablation_No_{skill.replace(' ', '_')}"
            ablation_metrics = summary.get(config_name, {})
            
            if not ablation_metrics:
                continue
            
            ablation_score = ablation_metrics.get("mean_score", 0)
            ablation_robustness = ablation_metrics.get("mean_robustness", 0)
            
            # Contribution = baseline - ablation
            score_contribution = baseline_score - ablation_score
            robustness_contribution = baseline_robustness - ablation_robustness
            
            contributions.append({
                "skill": skill,
                "score_contribution": score_contribution,
                "robustness_contribution": robustness_contribution,
                "combined": score_contribution + robustness_contribution
            })
            
            # Determine importance
            if score_contribution > 1.0:
                importance = "🔴 CRITICAL"
            elif score_contribution > 0.5:
                importance = "🟠 IMPORTANT"
            elif score_contribution > 0.2:
                importance = "🟡 BENEFICIAL"
            else:
                importance = "🟢 OPTIONAL"
            
            print(f"   {skill}:")
            print(f"      Score Impact: {score_contribution:+.2f} points")
            print(f"      Robustness Impact: {robustness_contribution:+.2f} points")
            print(f"      Importance: {importance}")
            print()
        
        # Rank by contribution
        contributions.sort(key=lambda x: x["combined"], reverse=True)
        
        print(f"🏆 Skill Ranking (Most Important → Least):")
        print()
        for i, contrib in enumerate(contributions, 1):
            print(f"   {i}. {contrib['skill']}")
            print(f"      Total Impact: {contrib['combined']:+.2f} points")
        print()
        
        analysis["skill_contributions"] = contributions
        analysis["rankings"] = [c["skill"] for c in contributions]
    
    return analysis


# Example usage
if __name__ == "__main__":
    # Run single-skill ablation
    results = run_skills_ablation_study(
        ablation_type="single",
        runs_per_question=3
    )
    
    print("\n" + "="*70)
    print("✅ ABLATION STUDY COMPLETE!")
    print("="*70)

