# Complete Directory Tree with Organization

Visual representation of the entire project structure with file categories and purposes.

---

## 📂 Full Project Structure

```
Algovant Internship/                          [PROJECT ROOT]
│
├── 📖 DOCUMENTATION FILES (English)
│   ├── README.md                              ← Main documentation (START HERE!)
│   ├── QUICKSTART.md                          ← 5-minute quick start
│   ├── API_REFERENCE.md                       ← Complete tool API
│   ├── PROJECT_STRUCTURE.md                   ← File organization guide
│   ├── FILE_ORGANIZATION.md                   ← How to extend the project
│   ├── DOCUMENTATION_INDEX.md                 ← Navigation guide
│   └── DIRECTORY_TREE.md                      ← This file
│
│
├── 🤖 MAIN ENTRY POINTS
│   ├── agent_main.py                          ← Primary agent (modular, recommended)
│   │                                          │ Initialize → Load tools → Build graph → CLI loop
│   │                                          │
│   └── agent_with_rules.py                    ← Alternative agent (rules-based)
│                                              │ Uses external markdown rule files
│
│
├── ⚙️ CONFIGURATION MANAGEMENT
│   └── config/
│       ├── __init__.py
│       └── settings.py                        ← Centralized configuration
│                                              │ • APIKeys class
│                                              │ • ModelConfig class
│                                              │ • Limits class
│                                              │ • Paths class
│                                              │ • RAGConfig class
│                                              │ • VisualizationConfig class
│                                              │ • AgentConfig class
│                                              │
│
├── 🔧 TOOLS & UTILITIES
│   └── tools/
│       ├── __init__.py
│       │
│       ├── code_execution.py                  ← Execute Python code
│       │                                      │ • Dynamic code execution
│       │                                      │ • Data analysis with libraries
│       │
│       ├── web_search.py                      ← Web search & assistance
│       │                                      │ • toolTavilySearch() - Web search
│       │                                      │ • human_assistance() - Request input
│       │
│       ├── search/                            ← OPTIONS DATA SEARCH TOOLS
│       │   ├── __init__.py
│       │   ├── options_search.py              ← Single ticker search (smart cache)
│       │   │                                  │ • search_options(ticker, date, limit)
│       │   │                                  │ • Checks knowledge base first
│       │   │                                  │ • Falls back to Polygon.io API
│       │   │
│       │   └── batch_search.py                ← Multiple tickers search
│       │                                      │ • batch_search_options(tickers, date)
│       │                                      │ • Efficient parallel requests
│       │
│       ├── export/                            ← DATA EXPORT TOOLS
│       │   ├── __init__.py
│       │   ├── csv_export.py                  ← CSV export
│       │   │                                  │ • make_option_table(data, ticker)
│       │   │                                  │ • Standard CSV format
│       │   │                                  │ • Saves to outputs/csv/
│       │   │
│       │   └── visualization.py               ← Chart generation
│       │                                      │ • plot_options_chain(data, ticker)
│       │                                      │ • PNG chart output
│       │                                      │ • Multiple chart types
│       │
│       └── analysis/                          ← PROFESSIONAL ANALYSIS TOOLS
│           ├── __init__.py
│           └── analysis_tools.py              ← Options analysis
│                                              │ • analyze_options_chain()
│                                              │ • generate_options_report()
│                                              │ • quick_sentiment_check()
│                                              │ • compare_options_sentiment()
│                                              │ • Greeks calculation
│                                              │ • Sentiment analysis
│                                              │
│
├── 📚 KNOWLEDGE BASE & RAG
│   └── rag/                                   [RETRIEVAL-AUGMENTED GENERATION]
│       ├── __init__.py
│       │
│       ├── rag_config.py                      ← RAG configuration
│       │                                      │ • ChromaDB path & collection
│       │                                      │ • Embedding model settings
│       │                                      │ • Search thresholds
│       │
│       ├── rag_knowledge_base.py              ← Core RAG implementation
│       │                                      │ • ChromaDB integration
│       │                                      │ • SQLite storage
│       │                                      │ • Embedding generation
│       │                                      │ • Semantic search
│       │                                      │ • Similarity matching
│       │
│       ├── rag_tools.py                       ← QUERY TOOLS
│       │                                      │ • store_options_data()
│       │                                      │ • search_knowledge_base()
│       │                                      │ • get_historical_options()
│       │                                      │ • get_snapshot_by_id()
│       │                                      │ • detect_anomaly()
│       │
│       └── rag_collection_tools.py            ← DATA COLLECTION TOOLS
│                                              │ • collect_and_store_options()
│                                              │ • batch_collect_options()
│                                              │ • collect_date_range()
│                                              │ • check_missing_data()
│                                              │ • auto_update_watchlist()
│                                              │
│
├── 📊 MONITORING & PERFORMANCE
│   └── monitoring/
│       ├── __init__.py
│       └── performance_monitor.py             ← Performance tracking
│                                              │ • start_tracking()
│                                              │ • record_tokens()
│                                              │ • record_tool_usage()
│                                              │ • get_performance_stats()
│                                              │ • Token usage metrics
│                                              │ • Tool execution times
│                                              │
│
├── 🧪 EVALUATION & TESTING
│   └── evaluation/
│       ├── __init__.py
│       ├── ab_testing_evaluator.py            ← A/B testing
│       │                                      │ • Compare configurations
│       │                                      │ • Performance comparison
│       │
│       ├── skills_ablation.py                 ← Skill importance analysis
│       │                                      │ • Test agent without tools
│       │                                      │ • Measure impact
│       │
│       ├── llm_judge.py                       ← LLM-based evaluation
│       │                                      │ • Quality assessment
│       │                                      │ • Response scoring
│       │
│       └── external_evaluator.py              ← External metrics
│                                              │ • Benchmark comparisons
│                                              │ • External datasets
│                                              │
│
├── 📈 ANALYSIS MODULES
│   └── analysis/
│       ├── __init__.py
│       └── options_analyzer.py                ← Domain-specific analysis
│                                              │ • Greeks interpretation
│                                              │ • Volatility analysis
│                                              │ • Sentiment calculation
│                                              │ • Risk assessment
│                                              │
│
├── 🛠️ UTILITY FUNCTIONS
│   └── utils/
│       ├── __init__.py
│       └── rules_loader.py                    ← Markdown rule file loader
│                                              │ • load_agent_rules()
│                                              │ • Rule file parsing
│                                              │ • Dynamic rule loading
│                                              │
│
├── 📏 BEHAVIORAL RULES (External Configuration)
│   └── rules/                                 [BEHAVIOR & METHODOLOGY]
│       ├── agent_rules.md                     ← Agent core rules & skills
│       │                                      │ • Core identity definition
│       │                                      │ • All skills defined
│       │                                      │ • Workflow procedures
│       │                                      │ • Tool selection logic
│       │
│       └── analysis_rules.md                  ← Professional analysis rules
│                                              │ • Analysis standards
│                                              │ • Greeks interpretation
│                                              │ • Sentiment methodology
│                                              │ • Report generation rules
│                                              │
│
├── 🌐 MICROSERVICE API
│   └── microservice/
│       ├── __init__.py (implicit)
│       ├── app.py                             ← FastAPI application
│       │                                      │ • REST API endpoints
│       │                                      │ • /api/search - Options search
│       │                                      │ • /api/csv - CSV export
│       │                                      │ • /api/chart - Chart generation
│       │                                      │ • /health - Health check
│       │                                      │ • /docs - API documentation
│       │
│       ├── docker-compose.yml                 ← Docker Compose config
│       │                                      │ • Multi-container setup
│       │
│       ├── Dockerfile                         ← Docker image definition
│       │                                      │ • Container configuration
│       │
│       ├── env.template                       ← Environment template
│       │                                      │ • Required environment variables
│       │
│       ├── requirements.txt                   ← Microservice dependencies
│       │                                      │ • FastAPI packages
│       │
│       ├── test_client.py                     ← API testing client
│       │                                      │ • Test endpoints
│       │
│       └── outputs/                           ← API-generated outputs
│                                              │ • CSV files from API calls
│                                              │ • Chart files from API calls
│                                              │
│
├── 📚 LEARNING EXAMPLES
│   ├── Week1/                                 [LEARNING & EXAMPLES]
│   │   ├── README.md                          ← Week 1 learning guide
│   │   │                                      │ • Environment setup
│   │   │                                      │ • File descriptions
│   │   │                                      │ • Learning path
│   │   │
│   │   ├── first_simple_openai_agent.py       ← Most basic agent
│   │   │                                      │ • Simple LangGraph setup
│   │   │
│   │   ├── using_prebuilt.py                  ← Prebuilt components
│   │   │                                      │ • ToolNode, tools_condition
│   │   │
│   │   ├── add_tavily.py                      ← Tool integration
│   │   │                                      │ • Adding web search
│   │   │
│   │   ├── added_time_travel.py               ← Memory persistence
│   │   │                                      │ • SqliteSaver, sessions
│   │   │
│   │   ├── add_customized_state.py            ← Advanced state management
│   │   │                                      │ • Custom State class
│   │   │
│   │   └── start-prebuiltagent.py             ← Alternative starter
│   │
│   ├── week2.py                               ← Week 2 example
│   │
│   └── langraph example/                      [LANGGRAPH REFERENCE]
│       └── path/to/your/app/
│           ├── src/agent/
│           │   └── graph.py                   ← Example graph
│           ├── tests/
│           │   ├── unit_tests/
│           │   └── integration_tests/
│           └── venv/                          ← Virtual environment
│
│
├── 💾 DATA STORAGE & PERSISTENCE
│   └── data/
│       │
│       ├── chroma_db/                         [VECTOR DATABASE]
│       │   ├── chroma.sqlite3                 ← ChromaDB storage
│       │   │                                  │ • Collection: options_snapshots
│       │   │                                  │ • 1536-D embeddings
│       │   │                                  │ • HNSW index
│       │   │
│       │   └── [collection_uuid]/             ← Collection data
│       │       ├── data_level0.bin
│       │       ├── header.bin
│       │       ├── length.bin
│       │       └── link_lists.bin
│       │
│       ├── conversation_memory.db             [CONVERSATION HISTORY]
│       │                                      │ • SQLite database
│       │                                      │ • Persists across sessions
│       │                                      │ • Messages & metadata
│       │
│       ├── conversation_memory.db-shm        ← SQLite shared memory
│       ├── conversation_memory.db-wal        ← Write-ahead log
│       │
│       ├── options.db                         [OPTIONS DATA CACHE]
│       │                                      │ • Cached options data
│       │                                      │ • Indexed by ticker/date
│       │
│       ├── embeddings_cache/                  [EMBEDDING CACHE]
│       │                                      │ • Cached embeddings
│       │                                      │ • Reduces API calls
│       │
│       └── evaluation_*.json                  [EVALUATION RESULTS]
│                                              │ • A/B test results
│                                              │ • Performance metrics
│                                              │ • Ablation study results
│                                              │
│
├── 📤 OUTPUT FILES & EXPORTS
│   └── outputs/
│       │
│       ├── csv/                               [EXPORTED CSV FILES]
│       │   └── [TICKER]_options_*.csv         • Standard CSV format
│       │                                      • Timestamped filenames
│       │
│       ├── charts/                            [GENERATED CHARTS]
│       │   └── [TICKER]_options_*.png         • PNG visualizations
│       │                                      • High resolution (100 DPI)
│       │
│       └── reports/                           [ANALYSIS REPORTS]
│           └── [TICKER]_analysis_*.json       • JSON format reports
│                                              • Professional analysis
│
│
├── 🛠️ UTILITY & MAINTENANCE SCRIPTS
│   ├── backup.py                              ← Backup utility
│   │                                          │ • Backup databases
│   │                                          │ • Backup configurations
│   │
│   ├── clear_memory.py                        ← Clear conversation memory
│   │                                          │ • Reset conversation history
│   │
│   └── code_examples/
│       └── csv_export_template.py             ← CSV export example
│                                              │ • Template for custom CSV
│
│
├── 📊 SAMPLE DATA FILES
│   └── NVDA_options_2025-11_*.csv             ← Sample options data
│
│
├── 📦 PROJECT CONFIGURATION
│   └── requirements.txt                       ← Python dependencies
│                                              │ • langchain==0.3.7
│                                              │ • langgraph==0.2.45
│                                              │ • openai==1.54.3
│                                              │ • chromadb==0.4.22
│                                              │ • matplotlib==3.8.2
│                                              │ • python-dotenv==1.0.0
│                                              │ • [and more...]
│
├── 🔐 ENVIRONMENT CONFIGURATION (Not in repo)
│   └── .env                                   ← API keys & secrets
│                                              │ OPENAI_API_KEY
│                                              │ POLYGON_API_KEY
│                                              │ TAVILY_API_KEY
│                                              │ ANTHROPIC_API_KEY
│
└── 🗂️ SYSTEM DIRECTORIES
    └── __pycache__/                           ← Python bytecode cache
                                               │ (Generated, ignore)


```

---

## 📊 Directory Summary Table

| Directory | Purpose | Key Files | Contains |
|-----------|---------|-----------|----------|
| **root** | Entry points | agent_main.py, requirements.txt | Executables, docs |
| **config/** | Settings | settings.py | APIKeys, Models, Paths, Limits |
| **tools/** | Tool suite | search/, export/, analysis/ | All agent tools |
| **tools/search/** | Data retrieval | options_search.py | Search + batch search |
| **tools/export/** | Output formats | csv_export.py, visualization.py | CSV + charts |
| **tools/analysis/** | Analysis | analysis_tools.py | Greeks, sentiment, reports |
| **rag/** | Knowledge base | rag_knowledge_base.py | ChromaDB + SQLite |
| **monitoring/** | Metrics | performance_monitor.py | Token tracking, stats |
| **evaluation/** | Testing | ab_testing_evaluator.py | A/B tests, ablation |
| **analysis/** | Domain logic | options_analyzer.py | Analysis functions |
| **utils/** | Helpers | rules_loader.py | Utility functions |
| **rules/** | Behavior specs | agent_rules.md | External rule files |
| **microservice/** | API | app.py | FastAPI endpoints |
| **Week1/** | Examples | *.py | Learning materials |
| **data/** | Persistence | *.db, chroma_db/ | Databases, cache |
| **outputs/** | Results | csv/, charts/ | Exports, reports |

---

## 🎯 File Type Legend

```
📖  Documentation (.md files)
🤖  Agent entry points (.py)
⚙️   Configuration (.py)
🔧  Tools & utilities (.py)
📚  Knowledge base (.py)
📊  Monitoring & evaluation (.py)
📈  Analysis (.py)
🛠️   Helper utilities (.py)
📏  Rules (markdown .md)
🌐  API & microservice (.py)
📚  Examples & learning (.py)
💾  Data storage (databases, json)
📤  Output files (csv, png, json)
```

---

## 📍 Quick File Locations

### Find Common Tasks

**To modify agent behavior:**
→ `rules/agent_rules.md` or `rules/analysis_rules.md`

**To add a new tool:**
→ `tools/[category]/new_tool.py`

**To change configuration:**
→ `config/settings.py`

**To integrate microservice:**
→ `microservice/app.py`

**To query knowledge base:**
→ `rag/rag_tools.py`

**To add new endpoint:**
→ `microservice/app.py`

**To run evaluation:**
→ `evaluation/` directory

**To understand system:**
→ Start with `README.md`

---

## 🔄 Data Flow Map

```
User Input
    ↓
agent_main.py
    ↓
    ├─→ tools/ (search, export, analysis)
    │   ├─→ Polygon.io API
    │   └─→ Local processing
    │
    ├─→ rag/ (knowledge base)
    │   ├─→ ChromaDB (embeddings)
    │   └─→ SQLite (structured data)
    │
    ├─→ monitoring/
    │   └─→ performance_monitor.py
    │
    └─→ Output
        ├─→ Console (CLI)
        ├─→ CSV files (outputs/csv/)
        ├─→ PNG charts (outputs/charts/)
        └─→ JSON reports (outputs/reports/)
```

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────┐
│      User Interface Layer           │
│  CLI / API / Integration            │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│    Agent Orchestration Layer        │
│  LangGraph + state management       │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Tool Execution Layer           │
│  Search, Export, Analysis, etc.     │
└────────────┬────────────────────────┘
             │
    ┌────────┼────────┬──────────┬──────────┐
    │        │        │          │          │
┌───▼──┐ ┌──▼────┐ ┌─▼──────┐ ┌─▼──┐ ┌───▼────┐
│ RAG  │ │Config │ │Monitor │ │Data│ │External│
│  KB  │ │Manager│ │ & Eval │ │Base│ │Services│
└──────┘ └───────┘ └────────┘ └────┘ └────────┘
```

---

## 📊 File Statistics

**Total Files:** 50+  
**Documentation:** 9 markdown files  
**Python Modules:** 30+ files  
**Config Files:** 2 files  
**Data Storage:** 3+ databases  
**Total Documentation:** 7000+ lines

---

## 🎓 Learning Sequence

```
Week1/
├─ first_simple_openai_agent.py    (Start here)
├─ using_prebuilt.py                (+Components)
├─ add_tavily.py                    (+Tools)
├─ added_time_travel.py             (+Memory)
└─ add_customized_state.py          (Advanced)
        ↓ (Understand basics)
    README.md                        (Full system)
        ↓ (Understand structure)
    PROJECT_STRUCTURE.md             (File organization)
        ↓ (Ready to develop)
    FILE_ORGANIZATION.md             (How to extend)
        ↓ (Ready to deploy)
    QUICKSTART.md / API_REFERENCE.md (Reference)
```

---

## ✅ Verification Checklist

Use this to verify the structure is complete:

- [ ] All .md documentation files present
- [ ] config/ contains settings.py
- [ ] tools/ organized into search/, export/, analysis/
- [ ] rag/ contains all RAG modules
- [ ] monitoring/ contains performance_monitor.py
- [ ] evaluation/ has all test modules
- [ ] microservice/ contains app.py
- [ ] rules/ has both markdown files
- [ ] data/ directory exists (can be empty)
- [ ] outputs/ directory exists with csv/, charts/, reports/
- [ ] Week1/ learning examples present
- [ ] requirements.txt present

---

## 🔗 Cross-References

**Key relationships:**
- `agent_main.py` imports everything
- `config/settings.py` used everywhere
- `tools/` contains all @tool functions
- `rag/` provides knowledge base
- `rules/` loaded by `agent_with_rules.py`
- `monitoring/` called from agent
- `evaluation/` used for testing

---

**Last Updated:** December 15, 2025  
**Structure Version:** 1.0.0  
**Status:** Organized & Documented ✅

