"""
Skills Ablation Study Runner
Author: Leo Ji

Run ablation studies to identify the contribution of each skill.
"""

from evaluation.skills_ablation import run_skills_ablation_study

def main():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🔬 Skills Ablation Study                                 ║
║                                                                    ║
║  Systematically test each skill's contribution to performance      ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")
    
    print("📚 What is Ablation Study?")
    print("   Remove components one by one → Measure performance drop")
    print("   → Identify which components are most critical")
    print()
    
    # Select ablation type
    print("=" * 70)
    print("STEP 1: SELECT ABLATION TYPE")
    print("=" * 70)
    print()
    print("📋 Ablation Types:")
    print()
    print("  1. Single Skill Ablation (推荐)")
    print("     Remove one skill at a time")
    print("     → Find which single skill is most important")
    print()
    print("  2. Cumulative Ablation")
    print("     Remove skills cumulatively")
    print("     → Find minimum necessary skill set")
    print()
    print("  3. Category Ablation")
    print("     Remove skills by category")
    print("     → Find which category is most important")
    print()
    
    ablation_choice = input("Select type (1-3) [default: 1]: ").strip() or "1"
    
    ablation_type_map = {
        "1": "single",
        "2": "cumulative",
        "3": "category"
    }
    
    ablation_type = ablation_type_map.get(ablation_choice, "single")
    
    print(f"\n✅ Selected: {ablation_type} ablation")
    
    # Select test questions
    print()
    print("=" * 70)
    print("STEP 2: SELECT TEST QUESTIONS")
    print("=" * 70)
    print()
    print("📝 Question sets:")
    print("  1. Mixed (search + analysis)")
    print("  2. Search-focused")
    print("  3. Analysis-focused")
    print("  4. Custom")
    print()
    
    question_choice = input("Select question set (1-4) [default: 1]: ").strip() or "1"
    
    if question_choice == "1":
        test_questions = [
            "Get AAPL options for December 2025",
            "Analyze TSLA options sentiment for November",
            "Compare NVDA and AMD options positioning"
        ]
    elif question_choice == "2":
        test_questions = [
            "Get AAPL options for December 2025",
            "Search for NVDA options in November",
            "Find MSFT options expiring in January 2026"
        ]
    elif question_choice == "3":
        test_questions = [
            "Analyze AAPL options sentiment for December",
            "Generate a professional report for TSLA options",
            "Compare sentiment between GOOGL and META options"
        ]
    else:
        print("\n✏️  Enter your questions (one per line, empty to finish):")
        test_questions = []
        while True:
            q = input(f"Question {len(test_questions)+1}: ").strip()
            if not q:
                break
            test_questions.append(q)
        
        if not test_questions:
            test_questions = [
                "Get AAPL options for December 2025",
                "Analyze TSLA sentiment",
                "Compare NVDA and AMD"
            ]
    
    print(f"\n📋 Test Questions:")
    for i, q in enumerate(test_questions, 1):
        print(f"   {i}. {q}")
    
    # Configure runs
    print()
    print("=" * 70)
    print("STEP 3: CONFIGURE ROBUSTNESS TESTING")
    print("=" * 70)
    print()
    print("🔄 Runs per question:")
    print("   3 runs - Quick (recommended for exploration)")
    print("   5 runs - Standard (recommended for validation)")
    print("   10 runs - Thorough (for critical decisions)")
    print()
    
    runs = input("Number of runs (1-10) [default: 3]: ").strip()
    try:
        runs_per_question = int(runs) if runs else 3
        runs_per_question = max(1, min(10, runs_per_question))
    except:
        runs_per_question = 3
    
    # Estimate time
    from evaluation.skills_ablation import SkillsAblator
    ablator = SkillsAblator("agent_rules.md")
    
    if ablation_type == "single":
        num_configs = len(ablator.skills) + 1  # +1 for baseline
    elif ablation_type == "cumulative":
        num_configs = len(ablator.skills) + 1
    else:
        num_configs = 4  # Baseline + 3 categories
    
    total_runs = num_configs * len(test_questions) * runs_per_question
    estimated_time = total_runs * 8  # ~8s per run
    
    print(f"\n📊 Test Summary:")
    print(f"   Configurations: {num_configs}")
    print(f"   Skills to test: {len(ablator.skills)}")
    print(f"   Questions: {len(test_questions)}")
    print(f"   Runs per question: {runs_per_question}")
    print(f"   Total runs: {total_runs}")
    print(f"   Estimated time: ~{estimated_time//60} minutes")
    
    # Confirm
    print()
    confirm = input("▶️  Start ablation study? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Run ablation study
    print()
    print("=" * 70)
    print("🔬 RUNNING ABLATION STUDY")
    print("=" * 70)
    print()
    
    try:
        results = run_skills_ablation_study(
            ablation_type=ablation_type,
            test_questions=test_questions,
            runs_per_question=runs_per_question
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Study interrupted (Ctrl+C)")
        return
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Summary
    print()
    print("=" * 70)
    print("🎯 ABLATION STUDY COMPLETE!")
    print("=" * 70)
    print()
    print(f"📄 Results saved: {results['filename']}")
    print()
    
    # Key findings
    if ablation_type == "single":
        analysis = results.get("analysis", {})
        rankings = analysis.get("rankings", [])
        
        if rankings:
            print("🔑 KEY FINDINGS:")
            print()
            print(f"   Most Critical Skill: {rankings[0]}")
            if len(rankings) > 1:
                print(f"   Least Critical Skill: {rankings[-1]}")
            print()
            print("   💡 Recommendation:")
            print(f"      • Must keep: {', '.join(rankings[:3])}")
            if len(rankings) > 5:
                print(f"      • Can consider removing: {', '.join(rankings[-2:])}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

