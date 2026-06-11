# Project Structure Documentation

## Complete File Organization Guide

This document provides a detailed breakdown of the entire project structure, explaining the purpose and relationships between all directories and files.

---

## Root Level Files

### `agent_main.py`
**Purpose**: Main entry point for the financial options analysis agent  
**Type**: Executable script  
**Status**: Production-ready (latest version)  
**Key Features**:
- Modular component assembly
- Tool loading and registration
- LangGraph graph construction
- Interactive CLI loop
- Performance monitoring integration

**Usage**:
```bash
python agent_main.py
```

### `agent_with_rules.py`
**Purpose**: Alternative agent using externalized rules from markdown files  
**Type**: Executable script  
**Status**: Production-ready (rules-based variant)  
**Key Features**:
- Dynamic rule loading from markdown files
- External rule file management
- Better maintainability for behavior updates
- Modular rules organization

**Usage**:
```bash
python agent_with_rules.py
```

**Related Files**:
- `utils/rules_loader.py` - Rule file loader

### `requirements.txt`
**Purpose**: Python package dependencies  
**Type**: Configuration file  
**Key Packages**:
- LangChain: Core AI framework
- LangGraph: Orchestration
- OpenAI: Language model
- Tavily: Web search
- ChromaDB: Vector database
- SQLAlchemy: Database ORM
- matplotlib: Visualization

### `README.md`
**Purpose**: Main project documentation  
**Comprehensive coverage of**:
- Project overview
- Feature descriptions
- Architecture diagrams
- Installation instructions
- Configuration guide
- Usage examples
- API reference
- Troubleshooting guide

---

## Core Directories

### `config/` - Configuration Management

```
config/
├── __init__.py           # Module initialization
└── settings.py          # Centralized configuration
```

#### **settings.py** - Configuration Classes

**APIKeys** class:
- `POLYGON_API_KEY` - Options data API
- `OPENAI_API_KEY` - GPT model access
- `TAVILY_API_KEY` - Web search API
- `ANTHROPIC_API_KEY` - Alternative LLM

**ModelConfig** class:
- `MODEL_NAME` - Current model selection
- `MODEL_PROVIDER` - API provider
- `TEMPERATURE` - LLM creativity level
- Judge model for evaluation

**Limits** class:
- Message history constraints
- Token limits
- Data limits (max contracts)
- API rate limits

**Paths** class:
- Directory structure definitions
- Database file paths
- Output directory paths
- `ensure_directories()` method

**RAGConfig** class:
- ChromaDB settings
- Embedding model configuration
- Search parameters
- Anomaly detection settings

**VisualizationConfig** class:
- Chart rendering settings
- Color schemes
- Figure dimensions

**AgentConfig** class:
- Thread ID for conversations
- Debug/verbose modes
- Monitoring settings

---

### `tools/` - Agent Tool Suite

```
tools/
├── __init__.py
├── code_execution.py          # Custom code execution
├── web_search.py              # Web search integration
│
├── search/                    # Options data search
│   ├── __init__.py
│   ├── options_search.py      # Single ticker search
│   └── batch_search.py        # Multiple tickers
│
├── export/                    # Data export functionality
│   ├── __init__.py
│   ├── csv_export.py          # CSV file generation
│   └── visualization.py       # Chart creation
│
└── analysis/                  # Analysis tools
    ├── __init__.py
    └── analysis_tools.py      # Options analysis
```

#### **search/options_search.py**
**Tool**: `search_options(ticker, date, limit, force_refresh)`
- Searches options data from Polygon.io
- Smart caching with knowledge base lookup
- Supports date (YYYY-MM-DD) or month (YYYY-MM) format
- Results: JSON with contract details

**Tool**: Additional search utilities
- Cache checking logic
- API fallback mechanisms
- Data parsing and formatting

#### **search/batch_search.py**
**Tool**: `batch_search_options(tickers, date, limit)`
- Efficient search for multiple tickers
- Parallel API calls
- Combined results in single response
- Useful for comparative analysis

#### **export/csv_export.py**
**Tool**: `make_option_table(data, ticker)`
- Converts JSON options data to CSV
- Standard column formatting
- Timestamp-based filenames
- Saves to `outputs/csv/` directory

**Output Format**:
- Expiration date, strike price, contract type (call/put)
- Greeks (delta, gamma, theta, vega)
- Bid/ask prices, implied volatility
- Open interest, volume

#### **export/visualization.py**
**Tool**: `plot_options_chain(data, ticker)`
- Generates PNG charts from options data
- Multiple visualization types:
  - Scatter plots: Strike vs implied volatility
  - Bar charts: Call/put volume comparison
  - Line charts: Price vs strike relationships
- Saves to `outputs/charts/` directory

#### **analysis/analysis_tools.py**
**Tools**: Professional analysis functions
1. `analyze_options_chain(ticker, options_data)`
   - Comprehensive chain analysis
   - Greeks analysis
   - Sentiment detection
   
2. `generate_options_report(ticker, format_type)`
   - Professional report generation
   - Formats: 'full', 'summary', 'json'
   
3. `quick_sentiment_check(ticker, options_data)`
   - Fast sentiment assessment
   - Call/put balance analysis
   
4. `compare_options_sentiment(ticker1, data1, ticker2, data2)`
   - Side-by-side comparison
   - Relative positioning analysis

#### **code_execution.py**
**Tool**: `code_execution_tool(code: str)`
- Execute custom Python code
- Access to data analysis libraries
- Perfect for advanced analysis
- Outputs results to console

#### **web_search.py**
**Tools**:
1. `toolTavilySearch(query)`
   - Web search using Tavily API
   - Get financial context
   - Company information lookup

2. `human_assistance(question)`
   - Request human input
   - For clarifications or decisions
   - Enables human-in-the-loop workflows

---

### `rag/` - Knowledge Base & RAG System

```
rag/
├── __init__.py
├── rag_config.py              # RAG configuration
├── rag_knowledge_base.py      # Core implementation
├── rag_tools.py               # Query tools
└── rag_collection_tools.py    # Collection tools
```

#### **rag_config.py**
**Configuration Parameters**:
- ChromaDB path and collection name
- SQLite database location
- Embedding model (OpenAI text-embedding-3-small)
- Search similarity thresholds
- Anomaly detection settings

#### **rag_knowledge_base.py**
**Core Functions**:
1. `generate_embedding(text)`
   - Creates OpenAI embeddings
   - 1536-dimensional vectors

2. `store_snapshot(ticker, date, data)`
   - Saves options data to ChromaDB and SQLite
   - Maintains historical records
   - Enables semantic search

3. `query_sqlite(ticker, start_date, end_date, limit)`
   - Structured data queries
   - Date range filtering
   - Fast retrieval

4. `search_by_similarity(query_text, limit)`
   - Semantic search using embeddings
   - Similarity scoring
   - Relevant document retrieval

#### **rag_tools.py**
**Tools for Knowledge Base Interaction**:
1. `store_options_data(ticker, date, data, note)`
   - Store in knowledge base
   - Add optional notes

2. `search_knowledge_base(query, limit)`
   - Semantic search
   - Natural language queries

3. `get_historical_options(ticker, start_date, end_date)`
   - Retrieve historical data
   - Date range queries

4. `get_snapshot_by_id(snapshot_id)`
   - Get specific snapshot
   - By unique identifier

5. `detect_anomaly(ticker, current_data)`
   - Find unusual changes
   - Vector similarity anomaly detection

#### **rag_collection_tools.py**
**Tools for Data Collection**:
1. `collect_and_store_options(ticker, date, limit)`
   - Search and store in one action

2. `batch_collect_options(tickers, date, limit)`
   - Collect multiple tickers
   - Store together

3. `collect_date_range(ticker, start_date, end_date, limit)`
   - Historical data collection
   - Multiple months/dates

4. `check_missing_data(ticker, start_date, end_date)`
   - Identify data gaps
   - Report missing dates

5. `auto_update_watchlist(tickers, limit)`
   - Automatic periodic collection
   - Maintain updated snapshots

---

### `monitoring/` - Performance Tracking

```
monitoring/
├── __init__.py
└── performance_monitor.py     # Performance metrics
```

#### **performance_monitor.py**
**PerformanceMonitor Class**:
- `start_tracking(user_input)` - Begin tracking
- `record_tokens(prompt, completion)` - Token count
- `record_tool_usage(tool_name)` - Tool invocation
- `stop_tracking()` - End tracking

**get_performance_stats() Tool**:
- Modes: "current", "summary", "history"
- Returns performance metrics
- Token usage, tool statistics

---

### `evaluation/` - Testing & Quality Assurance

```
evaluation/
├── __init__.py
├── ab_testing_evaluator.py    # A/B testing framework
├── external_evaluator.py      # External evaluation metrics
├── llm_judge.py               # LLM-based judgment
└── skills_ablation.py         # Skill ablation study
```

#### **ab_testing_evaluator.py**
- Compare two agent configurations
- Test different prompts or tools
- Measure performance differences
- Statistical significance testing

#### **skills_ablation.py**
- Test agent without specific tools
- Identify critical capabilities
- Measure performance impact

#### **llm_judge.py**
- Use LLM to evaluate responses
- Quality scoring
- Consistency checking

#### **external_evaluator.py**
- Integrate external metrics
- Benchmark against baselines
- Comparative analysis

**Running Evaluations**:
```bash
python run_evaluation.py      # Full suite
python run_ab_testing.py      # A/B testing
python run_skills_ablation.py # Skill impact
```

---

### `analysis/` - Domain-Specific Analysis

```
analysis/
├── __init__.py
└── options_analyzer.py        # Options analysis logic
```

#### **options_analyzer.py**
**Analysis Functions**:
- Greeks calculation and interpretation
- Implied volatility analysis
- Call/put ratio analysis
- Sentiment indicators
- Risk assessment

---

### `utils/` - Utility Functions

```
utils/
├── __init__.py
└── rules_loader.py            # Rule file loader
```

#### **rules_loader.py**
**Function**: `load_agent_rules(filename, as_system_prompt=True)`
- Loads markdown rule files
- Converts to system prompt
- Enables dynamic rule updates

---

### `rules/` - Behavioral Rules

```
rules/
├── agent_rules.md             # Core agent behaviors
└── analysis_rules.md          # Analysis methodologies
```

#### **agent_rules.md**
**Contents**:
- Core agent identity
- Skill definitions and triggers
- Workflow procedures
- Tool usage guidelines
- Interaction patterns
- Common ticker mappings

#### **analysis_rules.md**
**Contents**:
- Professional analysis standards
- Greeks interpretation
- Sentiment methodology
- Anomaly detection procedures
- Report generation standards

---

### `data/` - Data Storage & Persistence

```
data/
├── chroma_db/                 # Vector database
│   ├── chroma.sqlite3        # ChromaDB storage
│   └── [collection_files]/   # Embedding vectors
│
├── conversation_memory.db     # Conversation history
├── conversation_memory.db-shm # SQLite shared memory
├── conversation_memory.db-wal # SQLite write-ahead log
│
├── options.db                 # Options cache
│
├── embeddings_cache/          # Cached embeddings
│   └── [embedding_files].npy
│
└── evaluation_*.json          # Evaluation results
```

#### **Database Details**

**chroma_db/**: Vector embeddings for semantic search
- Collection: `options_snapshots`
- Dimension: 1536 (OpenAI embeddings)
- Index: HNSW for fast similarity search

**conversation_memory.db**: SQLite database
- Tables: messages, sessions, metadata
- Persists across agent restarts
- Enables session recovery

**options.db**: Options data cache
- Tables: options_snapshots, tickers, dates
- Indexed for fast queries
- Reduces API calls

---

### `outputs/` - Generated Results

```
outputs/
├── csv/                       # Exported CSV files
│   └── [TICKER]_options_*.csv
│
├── charts/                    # Generated PNG charts
│   └── [TICKER]_options_*.png
│
└── reports/                   # Analysis reports
    └── [TICKER]_analysis_*.json
```

---

### `microservice/` - FastAPI Service

```
microservice/
├── app.py                     # FastAPI application
├── docker-compose.yml         # Docker Compose config
├── Dockerfile                 # Docker image
├── env.template              # Environment template
├── requirements.txt          # Service dependencies
├── test_client.py            # Testing client
└── outputs/                  # API results
```

#### **app.py** - FastAPI Endpoints

**Endpoints**:
1. `POST /api/search` - Search options
2. `POST /api/csv` - Export CSV
3. `POST /api/chart` - Generate chart
4. `GET /health` - Health check
5. `GET /docs` - API documentation

**Request Models**:
- `SearchOptionsRequest`: ticker, date, limit
- `MakeCSVRequest`: data, ticker
- `PlotChartRequest`: data, ticker

#### **Docker Support**
- `Dockerfile`: Service containerization
- `docker-compose.yml`: Multi-container orchestration
- `env.template`: Environment variable template

---

### `Week1/` - Learning Examples

```
Week1/
├── README.md                           # Learning guide
├── first_simple_openai_agent.py       # Basic agent
├── using_prebuilt.py                  # Prebuilt components
├── add_tavily.py                      # Tool integration
├── added_time_travel.py               # Persistent memory
├── add_customized_state.py            # Advanced state
└── start-prebuiltagent.py             # Alternative start
```

**Learning Path**:
1. `first_simple_openai_agent.py` - Understand basics
2. `using_prebuilt.py` - Learn prebuilt components
3. `add_tavily.py` - Add tools
4. `added_time_travel.py` - Add persistence
5. `add_customized_state.py` - Advanced patterns

Each example builds on previous concepts.

---

### `langraph example/` - LangGraph Reference

Reference LangGraph project with:
- Example graph implementations
- Test cases
- Configuration examples
- Virtual environment setup

---

## Root Level Utility Scripts

### `backup.py`
**Purpose**: Backup project data  
**Backs up**: Databases, configurations, outputs  
**Usage**:
```bash
python backup.py
```

### `clear_memory.py`
**Purpose**: Clear conversation history  
**Clears**: SQLite conversation database  
**Usage**:
```bash
python clear_memory.py
```

### `week2.py`
**Purpose**: Week 2 learning example  
**Content**: Advanced agent concepts

---

## Data Files

### `NVDA_options_2025-11_*.csv`
**Purpose**: Sample options data  
**Type**: CSV export example  
**Use**: Testing and learning

---

## File Organization Summary

### By Category

#### **Executable Entry Points**
- `agent_main.py` - Main agent (modular)
- `agent_with_rules.py` - Rules-based agent
- `run_evaluation.py` - Evaluation runner
- `run_ab_testing.py` - A/B testing runner
- `run_skills_ablation.py` - Ablation study runner

#### **Configuration & Setup**
- `config/settings.py` - Central configuration
- `requirements.txt` - Dependencies
- `.env` - API keys (not in repo)
- `microservice/env.template` - Template

#### **Core Functionality**
- `agent_main.py` - Agent orchestration
- `tools/` - Tool implementations
- `rag/` - Knowledge base
- `analysis/` - Domain logic

#### **Data & Persistence**
- `data/` - All databases
- `outputs/` - Generated results
- Backup and cleanup scripts

#### **Testing & Evaluation**
- `evaluation/` - Test framework
- `Week1/` - Learning examples
- `microservice/test_client.py` - API testing

#### **Documentation**
- `README.md` - Main documentation
- `PROJECT_STRUCTURE.md` - This file
- `rules/` - Behavioral rules
- `Week1/README.md` - Learning guide

---

## Key Relationships

### Dependency Flow

```
agent_main.py
├── config/settings.py (imports)
├── tools/ (imports all tools)
│   ├── search/options_search.py
│   ├── export/csv_export.py
│   ├── analysis/analysis_tools.py
│   └── ...
├── rag/ (optional RAG tools)
│   └── rag_knowledge_base.py
└── monitoring/performance_monitor.py
```

### Data Flow

```
User Input
    ↓
agent_main.py (LangGraph)
    ↓
Tools (search, export, analysis)
    ↓
↙        ↘        ↘        ↘
Polygon.io  CSV  Chart  Knowledge Base
   (API)   (File)(File) (ChromaDB/SQLite)
```

### Configuration Hierarchy

```
settings.py
├── APIKeys (validation)
├── ModelConfig (LLM settings)
├── Limits (constraints)
├── Paths (directories)
├── RAGConfig (knowledge base)
├── VisualizationConfig (charts)
└── AgentConfig (behavior)
```

---

## Best Practices

### File Organization
1. Keep configuration centralized (`config/`)
2. Organize tools by functionality (`tools/search/`, `tools/export/`)
3. Separate concerns (tools, monitoring, evaluation)
4. Version control: exclude `data/`, `.env`

### Adding New Features
1. Create files in appropriate directories
2. Add configuration to `settings.py` if needed
3. Import in main agent file
4. Update documentation
5. Test thoroughly

### Maintenance
1. Regular backups (`backup.py`)
2. Monitor database size
3. Clean old evaluation results
4. Update rules as behavior improves
5. Document changes

---

## File Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| Python modules | 25+ | Core functionality |
| Configuration files | 2 | Settings, paths |
| Database files | 3+ | Persistence |
| Documentation | 3 | Guides, examples |
| Examples | 6 | Learning materials |
| Tools | 10+ | Agent capabilities |

---

**Last Updated**: December 15, 2025  
**Document Version**: 1.0

