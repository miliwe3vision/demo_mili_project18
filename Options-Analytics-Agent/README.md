# Financial Options Analysis Agent

A sophisticated AI-powered agent for real-time stock options data analysis, visualization, and intelligent caching. Built with LangChain, LangGraph, and ChromaDB for enterprise-level financial data processing.

**Author:** Leo Ji  
**Version:** 1.0.0  
**Last Updated:** December 2025

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Development](#development)
- [Evaluation & Testing](#evaluation--testing)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The **Financial Options Analysis Agent** is an intelligent conversational AI system designed to:

- **Search & Retrieve**: Real-time options data from Polygon.io with smart caching
- **Analyze**: Professional-grade options analysis with sentiment detection and anomaly detection
- **Export**: Multiple export formats (CSV, Charts, Reports)
- **Learn**: Persistent memory across sessions with SQLite
- **Scale**: Microservice architecture with FastAPI integration
- **Evaluate**: Built-in A/B testing, skill ablation, and performance monitoring

The agent uses LangGraph for orchestration, maintains long-term conversation memory, and provides multiple tools for data analysis and visualization.

---

## ✨ Key Features

### 1. **Intelligent Data Caching**
- Automatic knowledge base lookup before API calls
- Smart hybrid storage (ChromaDB + SQLite)
- Manual refresh option with `force_refresh=True`
- Reduces API usage and improves response time

### 2. **Persistent Memory**
- SQLite-based conversation history
- Multi-session continuity
- Remembers previous searches and preferences
- Survives program restarts

### 3. **Professional Analysis Tools**
- Options chain analysis with Greeks
- Sentiment analysis on options positioning
- Anomaly detection using vector similarity
- Comparative analysis across multiple tickers

### 4. **Flexible Export Options**
- Standard CSV export
- Custom CSV generation with code execution
- PNG chart visualization
- Professional reports in multiple formats

### 5. **RAG (Retrieval-Augmented Generation)**
- Knowledge base integration
- Semantic search on historical data
- Date range collection
- Automatic watchlist updates

### 6. **Performance Monitoring**
- Token usage tracking
- Tool execution metrics
- Query performance statistics
- A/B testing evaluators

### 7. **Microservice Integration**
- FastAPI endpoints for all tools
- Docker support
- RESTful API interface
- Easy scalability

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     User Interface                              │
│                 (CLI / API / Integration)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      LangGraph Agent                            │
│  ┌─────────────┐    ┌──────────┐    ┌──────────────────┐       │
│  │   Chatbot   │◄──►│  Tools   │◄──►│ LLM (GPT-4o)     │       │
│  │   Node      │    │  Node    │    │                  │       │
│  └─────────────┘    └──────────┘    └──────────────────┘       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬───────────────┐
        │                  │                  │               │
┌───────▼────────┐  ┌──────▼──────┐  ┌──────▼─────┐  ┌──────▼──────┐
│  Tool Suite    │  │ Memory/State│  │   RAG KB   │  │ Monitoring  │
│  - Search      │  │  - SQLite   │  │ -ChromaDB  │  │  - Metrics  │
│  - Export      │  │  - Session  │  │ -SQLite    │  │  - Tracking │
│  - Analysis    │  │  - History  │  │ -Embeddings│  │  - A/B Test │
│  - Web Search  │  │             │  │            │  │             │
└────────────────┘  └─────────────┘  └────────────┘  └─────────────┘
        │                   │                │              │
        └───────────────────┴────────────────┴──────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼─────────┐  ┌─────▼──────┐  ┌──────▼────────┐
│ Polygon.io API  │  │File Storage │  │ Microservice  │
│  (Options Data) │  │(CSV/Charts) │  │  (FastAPI)    │
└─────────────────┘  └─────────────┘  └───────────────┘
```

### Component Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM Orchestration** | LangGraph | Multi-agent workflow management |
| **Language Model** | GPT-4o (OpenAI) | Intelligent decision making |
| **Vector DB** | ChromaDB | Semantic similarity search |
| **Relational DB** | SQLite | Persistent storage |
| **API Framework** | FastAPI | Microservice endpoints |
| **Embeddings** | OpenAI Text Embedding 3-Small | Semantic encoding |
| **Data Source** | Polygon.io | Real-time options data |
| **Search** | Tavily Search | Web context retrieval |

---

## 📂 Project Structure

### Overview

```
Algovant Internship/
├── 📖 README.md (this file)
├── 📋 requirements.txt
│
├── 🤖 AGENT CORE
│   ├── agent_main.py                 # Main entry point (latest modular version)
│   └── agent_with_rules.py           # Rules-based agent with external markdown rules
│
├── ⚙️ CONFIG
│   ├── config/__init__.py
│   └── config/settings.py            # Centralized configuration
│
├── 🔧 TOOLS
│   ├── tools/__init__.py
│   ├── tools/code_execution.py       # Code execution tool
│   ├── tools/web_search.py           # Web search integration
│   │
│   ├── search/                       # Options search tools
│   │   ├── __init__.py
│   │   ├── options_search.py         # Single ticker search
│   │   └── batch_search.py           # Batch search for multiple tickers
│   │
│   ├── export/                       # Data export tools
│   │   ├── __init__.py
│   │   ├── csv_export.py             # CSV export functionality
│   │   └── visualization.py          # Chart generation
│   │
│   └── analysis/                     # Analysis tools
│       ├── __init__.py
│       └── analysis_tools.py         # Professional options analysis
│
├── 📚 RAG (Knowledge Base)
│   ├── rag/__init__.py
│   ├── rag_config.py                 # RAG system configuration
│   ├── rag_knowledge_base.py        # ChromaDB + SQLite implementation
│   ├── rag_tools.py                  # Query tools
│   └── rag_collection_tools.py       # Data collection tools
│
├── 📊 MONITORING & EVALUATION
│   ├── monitoring/
│   │   ├── __init__.py
│   │   └── performance_monitor.py    # Performance tracking
│   │
│   └── evaluation/
│       ├── __init__.py
│       ├── ab_testing_evaluator.py   # A/B testing
│       ├── external_evaluator.py     # External evaluations
│       ├── llm_judge.py              # LLM-based judge
│       └── skills_ablation.py        # Skill ablation study
│
├── 🎯 ANALYSIS MODULES
│   ├── analysis/__init__.py
│   └── options_analyzer.py           # Options analysis logic
│
├── 📏 UTILITIES
│   ├── utils/__init__.py
│   └── utils/rules_loader.py         # Rule file loader
│
├── 🌐 MICROSERVICE
│   ├── microservice/
│   │   ├── app.py                    # FastAPI application
│   │   ├── docker-compose.yml        # Docker compose config
│   │   ├── Dockerfile                # Docker image definition
│   │   ├── env.template              # Environment template
│   │   ├── requirements.txt           # Microservice dependencies
│   │   ├── test_client.py            # Testing client
│   │   └── outputs/                  # API output directory
│
├── 📚 RULES
│   ├── rules/
│   │   ├── agent_rules.md            # Core agent behaviors and workflows
│   │   └── analysis_rules.md         # Professional analysis rules
│
├── 📝 LEARNING EXAMPLES (Week 1)
│   ├── Week1/
│   │   ├── README.md
│   │   ├── first_simple_openai_agent.py
│   │   ├── using_prebuilt.py
│   │   ├── add_tavily.py
│   │   ├── added_time_travel.py
│   │   └── add_customized_state.py
│   └── week2.py
│
├── 📁 DATA STORAGE
│   ├── data/
│   │   ├── chroma_db/                # Vector database (ChromaDB)
│   │   ├── conversation_memory.db    # SQLite memory
│   │   ├── options.db                # Options cache
│   │   ├── embeddings_cache/         # Embedding cache
│   │   └── evaluation_*.json         # Evaluation results
│
├── 📤 OUTPUT
│   ├── outputs/
│   │   ├── csv/                      # Exported CSV files
│   │   ├── charts/                   # Generated PNG charts
│   │   └── reports/                  # Analysis reports
│
├── 🧪 TESTS & EVALUATION
│   ├── run_evaluation.py             # Run evaluation suite
│   ├── run_ab_testing.py             # Run A/B testing
│   ├── run_skills_ablation.py        # Run skill ablation
│   └── langraph example/             # LangGraph example project
│
├── 🛠️ UTILITIES & SCRIPTS
│   ├── backup.py                     # Backup utility
│   ├── clear_memory.py               # Memory cleanup
│   └── code_examples/
│       └── csv_export_template.py    # CSV export example
│
└── 📊 DATA FILES
    └── NVDA_options_*.csv            # Sample data files
```

### Key Directories Explained

#### **config/**
Centralized configuration management
- Environment variables
- API keys validation
- Model settings (GPT-4o selection)
- System limits (tokens, API calls)
- File paths organization
- Database connections

#### **tools/**
Complete tool suite for the agent
- **search/**: Options data retrieval (single and batch)
- **export/**: CSV export and chart visualization
- **analysis/**: Professional options analysis
- Additional tools: code execution, web search

#### **rag/**
Knowledge base and retrieval-augmented generation
- ChromaDB for vector similarity search
- SQLite for structured data persistence
- Collection tools for automated data gathering
- Query tools for knowledge retrieval
- Anomaly detection capabilities

#### **monitoring/**
Performance tracking and optimization
- Token usage metrics
- Tool execution statistics
- Query performance analysis
- Memory usage tracking

#### **evaluation/**
Quality assurance and testing
- A/B testing framework
- External evaluation metrics
- LLM judge for quality assessment
- Skill ablation studies

#### **data/**
All persistent storage
- SQLite databases (memory, options, evaluation)
- ChromaDB vector store
- Embedding cache
- JSON evaluation results

#### **outputs/**
Generated results and artifacts
- CSV exports in standardized format
- PNG charts and visualizations
- Analysis reports

---

## 💻 Installation

### Prerequisites

- **Python:** 3.9 or higher
- **pip:** Package manager
- **API Keys:**
  - OpenAI API Key (for GPT-4o)
  - Polygon.io API Key (for options data)
  - Tavily API Key (for web search)
  - Anthropic API Key (optional)

### Step 1: Clone & Navigate

```bash
cd /Users/leo/Desktop/CS\ projects/Algovant\ Internship
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

Create a `.env` file in the project root:

```bash
# Copy template
cp .env.template .env

# Edit with your keys
nano .env  # or use your preferred editor
```

Fill in the `.env` file with your API keys:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx

# Polygon.io API Key (required)
POLYGON_API_KEY=your_polygon_key_here

# Tavily Search API Key (optional)
TAVILY_API_KEY=your_tavily_key_here

# Anthropic API Key (optional)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

### Step 5: Verify Installation

```bash
python agent_main.py
```

You should see initialization messages confirming all components are loaded.

---

## ⚙️ Configuration

### Main Configuration File: `config/settings.py`

The system uses a centralized `Settings` class with multiple configuration categories:

#### **API Keys** (`APIKeys`)
```python
POLYGON_API_KEY      # Options data API
OPENAI_API_KEY       # Language model
TAVILY_API_KEY       # Web search
ANTHROPIC_API_KEY    # Alternative LLM
```

#### **Model Configuration** (`ModelConfig`)
```python
MODEL_NAME = "gpt-4o-mini"        # Current model
MODEL_PROVIDER = "openai"         # Provider
TEMPERATURE = 0.7                 # Creativity level
JUDGE_MODEL_NAME = "gpt-4o-mini"  # For evaluation
```

#### **System Limits** (`Limits`)
```python
MAX_MESSAGES = 20                 # Conversation history
MAX_CONTEXT_TOKENS = 128000       # Token limit
SAFE_CONTEXT_TOKENS = 80000       # Conservative limit
MAX_OPTIONS_CONTRACTS = 1000      # Data limit
DEFAULT_OPTIONS_LIMIT = 100       # Default contracts
```

#### **RAG Configuration** (`RAGConfig`)
```python
COLLECTION_NAME = "options_snapshots"
EMBEDDING_MODEL = "text-embedding-3-small"
MIN_SIMILARITY_THRESHOLD = 0.7
ANOMALY_DETECTION_ENABLED = True
```

### Customizing Configuration

Edit `config/settings.py` to modify:

```python
# Example: Change default model
class ModelConfig:
    MODEL_NAME = "gpt-4"  # Instead of "gpt-4o-mini"

# Example: Increase context history
class Limits:
    MAX_MESSAGES = 50  # Instead of 20

# Example: Adjust RAG sensitivity
class RAGConfig:
    MIN_SIMILARITY_THRESHOLD = 0.5  # More lenient matching
```

---

## 🚀 Usage

### Option 1: Interactive CLI Agent

**Start the main agent:**

```bash
python agent_main.py
```

Or use the rules-based version:

```bash
python agent_with_rules.py
```

**Typical interaction flow:**

```
User: Get options for AAPL on 2025-12-19
Agent: I'll search for Apple options expiring on December 19, 2025.
       How many contracts would you like? (default: 100, max: 1000)

User: 200
Agent: Found 200 options contracts. What would you like to do?
       - 📊 Export to CSV
       - 📈 Generate chart
       - 💬 Show summary
       - 📋 Both CSV and chart

User: Both CSV and chart
Agent: Creating exports...
       ✅ CSV saved: outputs/csv/AAPL_options_2025-12_20251215_143022.csv
       ✅ Chart saved: outputs/charts/AAPL_options_2025-12.png
```

### Option 2: Microservice API

**Start the FastAPI server:**

```bash
cd microservice
python app.py

# Or using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**API Endpoints:**

```bash
# Search options
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "date": "2025-12-19", "limit": 100}'

# Export CSV
curl -X POST "http://localhost:8000/api/csv" \
  -H "Content-Type: application/json" \
  -d '{"data": {...}, "ticker": "AAPL"}'

# Generate chart
curl -X POST "http://localhost:8000/api/chart" \
  -H "Content-Type: application/json" \
  -d '{"data": {...}, "ticker": "AAPL"}'
```

### Option 3: Python Integration

```python
from agent_main import graph, config, stream_graph_updates

# Use in your Python code
stream_graph_updates("Get options for AAPL on 2025-12-19")
```

### Option 4: Learning with Examples

```bash
# Week 1 examples (basic to advanced)
cd Week1
python first_simple_openai_agent.py      # Most basic
python using_prebuilt.py                 # With prebuilt components
python add_tavily.py                     # With web search
python added_time_travel.py              # With memory
python add_customized_state.py           # Advanced state
```

---

## 🛠️ API Reference

### Core Tools

#### **search_options()**
Search for options data with smart caching
```python
@tool
def search_options(
    ticker: str,              # Stock symbol (e.g., "AAPL")
    date: str,               # YYYY-MM-DD or YYYY-MM format
    limit: int = 300,        # Number of contracts (1-1000)
    force_refresh: bool = False  # Skip cache if True
) -> str:  # Returns JSON with options data
```

**Example:**
```python
result = search_options("AAPL", "2025-12-19", limit=200)
```

#### **batch_search_options()**
Search multiple tickers efficiently
```python
@tool
def batch_search_options(
    tickers: list,           # ["AAPL", "TSLA", "MSFT"]
    date: str,              # Same date for all tickers
    limit: int = 100
) -> str:  # Returns dict with results for each ticker
```

#### **make_option_table()**
Export options data to CSV
```python
@tool
def make_option_table(
    data: str,              # JSON data from search_options
    ticker: str             # Stock symbol
) -> str:  # Returns success message with filename
```

#### **plot_options_chain()**
Generate PNG chart visualization
```python
@tool
def plot_options_chain(
    data: str,              # JSON data from search_options
    ticker: str             # Stock symbol
) -> str:  # Returns success message with filename
```

#### **analyze_options_chain()**
Professional options analysis
```python
@tool
def analyze_options_chain(
    ticker: str,            # Stock symbol (must be first!)
    options_data: str       # JSON data
) -> str:  # Returns detailed analysis report
```

#### **collect_and_store_options()**
Collect and immediately store in knowledge base
```python
@tool
def collect_and_store_options(
    ticker: str,            # Stock symbol
    date: str,             # YYYY-MM-DD or YYYY-MM
    limit: int             # Number of contracts
) -> str:  # Returns storage confirmation
```

#### **search_knowledge_base()**
Query the knowledge base
```python
@tool
def search_knowledge_base(
    query: str,             # Natural language query
    limit: int = 5          # Max results
) -> str:  # Returns matching historical data
```

#### **detect_anomaly()**
Find unusual changes in options data
```python
@tool
def detect_anomaly(
    ticker: str,           # Stock symbol
    current_data: str      # Current options data
) -> str:  # Returns anomaly report
```

### Utility Tools

#### **code_execution_tool()**
Execute custom Python code
```python
@tool
def code_execution_tool(code: str) -> str:
    """Execute custom Python code for advanced analysis"""
```

#### **get_performance_stats()**
Get system performance metrics
```python
@tool
def get_performance_stats(
    mode: str = "current"  # "current", "summary", or "history"
) -> str:  # Returns performance metrics
```

#### **human_assistance()**
Request human input
```python
@tool
def human_assistance(question: str) -> str:
    """Ask for human intervention when needed"""
```

---

## 👨‍💻 Development

### Project Architecture Principles

1. **Modularity**: Each tool and component is independent
2. **Configurability**: Settings centralized in `config/settings.py`
3. **Extensibility**: Easy to add new tools and rules
4. **Maintainability**: Clear separation of concerns
5. **Observability**: Built-in monitoring and logging

### Adding a New Tool

**Step 1:** Create a new file in `tools/`:

```python
# tools/my_new_tool.py
from langchain_core.tools import tool

@tool
def my_new_tool(parameter: str) -> str:
    """
    Tool description for the LLM.
    
    Args:
        parameter: What this parameter does
    
    Returns:
        What the tool returns
    """
    # Implementation
    return "Result"
```

**Step 2:** Import and register in `agent_main.py`:

```python
from tools.my_new_tool import my_new_tool

tools = [
    # ... existing tools ...
    my_new_tool,  # Add here
]
```

### Adding New Rules

**Step 1:** Edit `rules/agent_rules.md` or create new markdown file:

```markdown
## 🎯 New Capability: My New Skill

### Description
What this skill does...

### Workflow
1. First step
2. Second step
3. Third step

### Tools Used
- tool_name_1
- tool_name_2
```

**Step 2:** Load rules in agent:

```python
# In agent_with_rules.py
agent_rules = load_agent_rules("agent_rules.md")
# New rules automatically included
```

### Extending Configuration

Add new configuration class in `config/settings.py`:

```python
class MyNewConfig:
    """Configuration for my new feature"""
    SETTING_1 = "value"
    SETTING_2 = 100
    
# Add to Settings class
class Settings:
    my_feature = MyNewConfig
    
# Export
MY_FEATURE_CONFIG = settings.my_feature
```

### Database Management

**Check database contents:**

```bash
# SQLite databases
sqlite3 data/conversation_memory.db ".tables"
sqlite3 data/options.db ".schema"

# ChromaDB (Python)
python
>>> from rag.rag_knowledge_base import client
>>> collections = client.list_collections()
```

**Backup data:**

```bash
python backup.py
```

**Clear conversation memory:**

```bash
python clear_memory.py
```

---

## 📊 Evaluation & Testing

### Running Evaluations

**A/B Testing:**

```bash
python run_ab_testing.py
```

Compares performance of different agent configurations or prompts.

**Skill Ablation Study:**

```bash
python run_skills_ablation.py
```

Tests the agent's performance with different tool subsets to identify critical skills.

**External Evaluation:**

```bash
python run_evaluation.py
```

Uses external datasets and metrics for comprehensive evaluation.

### Monitoring Performance

**In-Agent Performance Stats:**

```python
# Ask the agent
User: What are my performance statistics?
Agent: [Returns token usage, tool execution metrics, query performance]
```

**View Evaluation Results:**

```bash
# Check evaluation JSON files
cat data/evaluation_*.json | python -m json.tool
```

---

## 🐛 Troubleshooting

### Common Issues

#### **Issue: API Key Not Found**

```
Error: Missing required API keys: POLYGON_API_KEY, OPENAI_API_KEY
```

**Solution:**
1. Verify `.env` file exists in project root
2. Check API keys are correct
3. Run: `python -c "from config.settings import settings; settings.initialize()"`

#### **Issue: ChromaDB Connection Error**

```
Error: Failed to connect to ChromaDB
```

**Solution:**
```bash
# Clear and reinitialize
rm -rf data/chroma_db
python agent_main.py  # Will recreate
```

#### **Issue: SQLite Database Locked**

```
Error: database is locked
```

**Solution:**
```bash
# Close other connections and clear locks
rm -f data/conversation_memory.db-*
python agent_main.py
```

#### **Issue: Context Length Exceeded**

```
Error: This model's maximum context length is...
```

**Solution:**
Adjust `MAX_MESSAGES` in `config/settings.py`:
```python
class Limits:
    MAX_MESSAGES = 10  # Reduce from default 20
```

#### **Issue: Polygon.io Rate Limiting**

```
Error: API rate limit exceeded
```

**Solution:**
- Use caching with `force_refresh=False` (default)
- Increase delay between requests
- Upgrade Polygon.io API plan

#### **Issue: Microservice Port in Use**

```
Error: Address already in use (:8000)
```

**Solution:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn microservice.app:app --port 8001
```

### Debug Mode

Enable verbose logging:

```python
# In config/settings.py
class AgentConfig:
    DEBUG = True
    VERBOSE = True
```

Or run with Python debugging:

```bash
python -m pdb agent_main.py
```

### Performance Optimization

**Reduce Context Length:**
```python
# config/settings.py
MAX_MESSAGES = 10  # Default 20
```

**Disable Monitoring (for speed):**
```python
ENABLE_PERFORMANCE_MONITORING = False
```

**Use Smaller Model:**
```python
MODEL_NAME = "gpt-4o-mini"  # Faster and cheaper than gpt-4
```

**Increase Cache Hit Rate:**
```python
# RAG tuning
MIN_SIMILARITY_THRESHOLD = 0.5  # More lenient matching
```

---

## 📚 Additional Resources

### Learning Paths

1. **For Beginners**: Start with `Week1/` examples
   - Basic LangGraph concepts
   - State management
   - Tool integration

2. **For Intermediate**: Study `agent_main.py`
   - Modular architecture
   - Tool assembly
   - Memory management

3. **For Advanced**: Explore evaluation framework
   - A/B testing
   - Skill ablation
   - Performance metrics

### Documentation Files

- **Agent Rules**: `rules/agent_rules.md` - Core behaviors
- **Analysis Rules**: `rules/analysis_rules.md` - Analysis methodology
- **Week 1 Examples**: `Week1/README.md` - Learning materials

### External Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Polygon.io API Docs](https://polygon.io/docs/stocks/getting-started)

---

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` file or API keys to version control
2. **Database Access**: SQLite files contain conversation history (sensitive data)
3. **Rate Limiting**: Implement rate limiting in production
4. **Input Validation**: Sanitize user inputs before processing
5. **HTTPS**: Use HTTPS for microservice API in production

---

## 📈 Performance Benchmarks

| Metric | Typical Value |
|--------|--------------|
| Search Response (cached) | < 500ms |
| Search Response (API call) | 1-3 seconds |
| CSV Export | < 1 second |
| Chart Generation | 2-5 seconds |
| Analysis Report | 5-10 seconds |
| Token Usage (per query) | 500-2000 tokens |

---

## 📝 License & Attribution

**Project**: Financial Options Analysis Agent  
**Author**: Leo Ji  
**Organization**: Algovant Internship  
**Date**: December 2025

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- [ ] Additional analysis indicators (Greeks, IV rank, etc.)
- [ ] More visualization types (heatmaps, Greeks profiles)
- [ ] Real-time WebSocket support
- [ ] Database query optimization
- [ ] Additional evaluation metrics
- [ ] Deployment automation
- [ ] Multi-language support
- [ ] Mobile app integration

---

## 💬 Support

For issues or questions:

1. Check the **Troubleshooting** section
2. Review relevant documentation files
3. Check Week1 examples for learning resources
4. Review evaluation results for performance insights

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅

