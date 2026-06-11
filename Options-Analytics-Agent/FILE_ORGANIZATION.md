# File Organization Guide

This document explains the systematic organization of the Financial Options Analysis Agent project and recommendations for maintaining and extending it.

---

## 📊 Current Organization Overview

The project is organized into **11 main categories** by functionality:

```
Algovant Internship/
├── 🤖 Agent Entry Points          (agent_main.py, agent_with_rules.py)
├── ⚙️  Configuration              (config/)
├── 🔧 Tools & Utilities           (tools/)
├── 📚 Knowledge Base              (rag/)
├── 📊 Monitoring & Evaluation     (monitoring/, evaluation/)
├── 📁 Analysis Logic              (analysis/)
├── 🛠️  Helper Utilities            (utils/)
├── 📏 Behavioral Rules            (rules/)
├── 🌐 Microservice API            (microservice/)
├── 📖 Documentation              (README.md, *.md files)
└── 💾 Data & Outputs             (data/, outputs/)
```

---

## 1️⃣ Agent Entry Points

**Location:** Project root  
**Files:**
- `agent_main.py` - Main modular agent (recommended)
- `agent_with_rules.py` - Rules-based agent variant

**Purpose:** User-facing executables to start the agent  
**When to modify:** Add new main features or entry points

---

## 2️⃣ Configuration Management

**Location:** `config/`

```
config/
├── __init__.py              # Module initialization
└── settings.py              # Centralized configuration
```

### `settings.py` Structure

The file is organized into **configuration classes**:

```python
# 1. API Keys - External service credentials
class APIKeys:
    POLYGON_API_KEY
    OPENAI_API_KEY
    TAVILY_API_KEY
    ANTHROPIC_API_KEY
    
    @classmethod
    def validate(cls):        # Validates required keys

# 2. Model Configuration - LLM settings
class ModelConfig:
    MODEL_NAME                # Current model selection
    MODEL_PROVIDER            # API provider
    TEMPERATURE               # Creativity level
    JUDGE_MODEL_NAME          # For evaluation

# 3. System Limits - Resource constraints
class Limits:
    MAX_MESSAGES              # Conversation history
    MAX_CONTEXT_TOKENS        # Token limits
    MAX_OPTIONS_CONTRACTS     # Data limits
    POLYGON_API_RATE_LIMIT    # API rate limits

# 4. File Paths - Directory structure
class Paths:
    DATA_DIR, CHROMA_DB_DIR, CSV_DIR, etc.
    
    @classmethod
    def ensure_directories(cls):  # Creates directories

# 5. RAG Configuration - Knowledge base settings
class RAGConfig:
    COLLECTION_NAME           # ChromaDB collection
    EMBEDDING_MODEL           # Embedding model
    MIN_SIMILARITY_THRESHOLD  # Search threshold

# 6. Visualization Configuration - Chart settings
class VisualizationConfig:
    MATPLOTLIB_BACKEND        # Chart backend
    DEFAULT_FIGURE_SIZE       # Chart dimensions
    COLOR_SCHEME              # Call/Put colors

# 7. Agent Configuration - Behavior settings
class AgentConfig:
    DEFAULT_THREAD_ID         # Session ID
    DEBUG, VERBOSE            # Debug flags
    ENABLE_PERFORMANCE_MONITORING

# Global Settings - Aggregator
class Settings:
    api_keys = APIKeys
    model = ModelConfig
    limits = Limits
    paths = Paths
    rag = RAGConfig
    visualization = VisualizationConfig
    agent = AgentConfig
    
    @classmethod
    def initialize(cls):      # Initialization hook
```

### How to Modify Configuration

**For API Keys:**
```bash
# Create .env file with your keys
OPENAI_API_KEY=sk-proj-...
POLYGON_API_KEY=pk-...
```

**For Model Settings:**
Edit `config/settings.py`:
```python
class ModelConfig:
    MODEL_NAME = "gpt-4"  # Change from gpt-4o-mini
    TEMPERATURE = 0.5     # Make more deterministic
```

**For New Configuration:**
```python
# Add new class in settings.py
class MyNewConfig:
    SETTING_1 = "value"
    SETTING_2 = 100

# Add to Settings aggregator
class Settings:
    my_new_config = MyNewConfig

# Export
MY_NEW_CONFIG = settings.my_new_config
```

---

## 3️⃣ Tools & Utilities

**Location:** `tools/`

```
tools/
├── __init__.py
├── code_execution.py          # Code execution tool
├── web_search.py              # Web search integration
│
├── search/                    # Options search
│   ├── __init__.py
│   ├── options_search.py      # Single ticker search
│   └── batch_search.py        # Batch search
│
├── export/                    # Data export
│   ├── __init__.py
│   ├── csv_export.py          # CSV export
│   └── visualization.py       # Chart generation
│
└── analysis/                  # Analysis tools
    ├── __init__.py
    └── analysis_tools.py      # Options analysis
```

### Organization Principles

1. **By Functionality**: Each subdirectory handles one function
   - `search/` - Data retrieval
   - `export/` - Output formats
   - `analysis/` - Data interpretation

2. **Modular Design**: Each tool is independent
   - Can be imported individually
   - Can be reused in other projects
   - No circular dependencies

3. **Tool Decoration**: All exposed functions use `@tool` decorator
   ```python
   from langchain_core.tools import tool
   
   @tool
   def my_tool(parameter: str) -> str:
       """Documentation for LLM"""
       return result
   ```

### Adding New Tools

**Step 1:** Create file in appropriate subdirectory

```bash
# For data retrieval
touch tools/search/new_search_tool.py

# For output format
touch tools/export/new_export_tool.py

# For analysis
touch tools/analysis/new_analysis_tool.py
```

**Step 2:** Implement with @tool decorator

```python
# tools/search/my_search.py
from langchain_core.tools import tool

@tool
def my_search_tool(ticker: str, date: str) -> str:
    """Search implementation"""
    return json.dumps(result)
```

**Step 3:** Register in agent

```python
# In agent_main.py
from tools.search.my_search import my_search_tool

tools = [
    # ... existing tools ...
    my_search_tool,  # Add here
]
```

---

## 4️⃣ Knowledge Base (RAG)

**Location:** `rag/`

```
rag/
├── __init__.py
├── rag_config.py              # RAG configuration
├── rag_knowledge_base.py      # Core implementation
├── rag_tools.py               # Query tools
└── rag_collection_tools.py    # Collection tools
```

### Component Relationships

```
rag_config.py          ← Configuration parameters
         ↓
rag_knowledge_base.py  ← Core storage/search logic
         ↓
    ┌────┴─────┐
    ↓          ↓
rag_tools.py  rag_collection_tools.py
(Queries)     (Data Collection)
```

### Data Storage Architecture

**ChromaDB** (Vector similarity)
- Collections: `options_snapshots`
- Embeddings: 1536-D vectors
- Index: HNSW (fast search)
- Use: Semantic similarity search

**SQLite** (Structured queries)
- Tables: options_snapshots, metadata
- Index: ticker, date
- Use: Time-range queries

### Adding RAG Features

1. **New Query Type**: Add to `rag_tools.py`
2. **New Collection Strategy**: Add to `rag_collection_tools.py`
3. **New Storage Format**: Extend `rag_knowledge_base.py`

---

## 5️⃣ Monitoring & Evaluation

**Location:** `monitoring/` and `evaluation/`

```
monitoring/
├── __init__.py
└── performance_monitor.py     # Metrics tracking

evaluation/
├── __init__.py
├── ab_testing_evaluator.py    # A/B testing
├── external_evaluator.py      # External metrics
├── llm_judge.py               # LLM judge
└── skills_ablation.py         # Ablation study
```

### Metrics Collected

**performance_monitor.py tracks:**
- Token usage (prompt + completion)
- Tool execution time
- Tool invocation count
- Query performance

**Evaluation scripts measure:**
- Response quality
- Tool effectiveness
- Agent skill importance
- Performance benchmarks

---

## 6️⃣ Analysis Logic

**Location:** `analysis/`

```
analysis/
├── __init__.py
└── options_analyzer.py        # Domain-specific analysis
```

**Contains:** Options-specific calculations
- Greeks interpretation
- Volatility analysis
- Sentiment detection
- Risk assessment

---

## 7️⃣ Utility Functions

**Location:** `utils/`

```
utils/
├── __init__.py
└── rules_loader.py            # Markdown rule loader
```

**Contains:** Helper functions used across the project

### Adding Utilities

Create new files in `utils/`:
```python
# utils/my_helper.py
def my_utility_function():
    """Helper function"""
    pass

# Import in agent
from utils.my_helper import my_utility_function
```

---

## 8️⃣ Behavioral Rules

**Location:** `rules/`

```
rules/
├── agent_rules.md             # Core behaviors
└── analysis_rules.md          # Analysis methodology
```

### Rule File Organization

**agent_rules.md** sections:
```markdown
# Agent Rules and Skills

## 🎯 Core Identity
- Role definition
- Capabilities
- Personality

## 📚 Skill: [Skill Name]
- Description
- Triggers
- Workflow
- Tools Used

## [More Skills...]
```

**analysis_rules.md** sections:
```markdown
# Analysis Rules

## Professional Standards
## Greeks Interpretation
## Sentiment Methodology
## Report Format
```

### Adding New Rules

1. **Edit markdown file**:
   ```bash
   nano rules/agent_rules.md
   ```

2. **Add new skill section**:
   ```markdown
   ## 📚 Skill: New Skill Name
   
   ### Description
   What this skill does
   
   ### Workflow
   Step-by-step procedure
   
   ### Tools
   - tool_1
   - tool_2
   ```

3. **Rules automatically reload** on agent restart

---

## 9️⃣ Microservice API

**Location:** `microservice/`

```
microservice/
├── app.py                     # FastAPI application
├── docker-compose.yml         # Docker Compose
├── Dockerfile                 # Docker image
├── env.template              # Environment template
├── requirements.txt          # Dependencies
├── test_client.py            # Test client
└── outputs/                  # API outputs
```

### FastAPI Structure

**app.py contains:**
```python
# 1. FastAPI instance
app = FastAPI(...)

# 2. Request/Response models
class SearchOptionsRequest(BaseModel):
    ticker: str
    date: str
    limit: int = 100

# 3. API endpoints
@app.post("/api/search")
async def search_endpoint(request: SearchOptionsRequest):
    ...

# 4. Tool implementations
def search_polygon(ticker, date, limit):
    ...
```

### Adding New API Endpoints

1. **Define request model**:
   ```python
   class MyRequest(BaseModel):
       param1: str
       param2: int
   ```

2. **Create endpoint**:
   ```python
   @app.post("/api/my-endpoint")
   async def my_endpoint(request: MyRequest):
       result = do_something(request.param1)
       return {"status": "success", "data": result}
   ```

3. **Test endpoint**:
   ```bash
   curl -X POST "http://localhost:8000/api/my-endpoint" \
     -H "Content-Type: application/json" \
     -d '{"param1": "value", "param2": 100}'
   ```

---

## 🔟 Documentation

**Location:** Project root

```
README.md                      # Main documentation
QUICKSTART.md                  # Quick start guide
API_REFERENCE.md              # Complete API docs
PROJECT_STRUCTURE.md          # Structure overview
FILE_ORGANIZATION.md          # This file
Week1/README.md               # Learning guide
```

### Documentation Organization

1. **README.md** - Complete guide
   - Overview and features
   - Installation
   - Configuration
   - Usage
   - Troubleshooting

2. **QUICKSTART.md** - Fast setup
   - 30-second installation
   - First interaction
   - Common use cases

3. **API_REFERENCE.md** - Tool documentation
   - All tools listed
   - Parameters and returns
   - Examples for each

4. **PROJECT_STRUCTURE.md** - Code organization
   - Directory breakdown
   - File purposes
   - Key relationships

5. **FILE_ORGANIZATION.md** - This guide
   - How to extend
   - Best practices
   - Adding features

---

## 1️⃣1️⃣ Data Storage

**Location:** `data/` and `outputs/`

```
data/
├── chroma_db/                 # Vector database
│   ├── chroma.sqlite3
│   └── [collection_data]/
├── conversation_memory.db     # Conversation history
├── conversation_memory.db-*   # WAL files
├── options.db                 # Options cache
├── embeddings_cache/          # Embedding cache
└── evaluation_*.json          # Results

outputs/
├── csv/                       # Exported CSV files
├── charts/                    # Generated PNG charts
└── reports/                   # Analysis reports
```

### Data Organization Rules

**Don't modify directly:**
- `chroma_db/` - ChromaDB internal files
- `*.db-*` files - SQLite temporary files

**Safe to manage:**
- Delete old CSV/chart files
- Archive evaluation results
- Backup `.db` files

**For cleanup:**
```bash
# Backup before cleanup
python backup.py

# Clear conversation history
python clear_memory.py

# Clear old CSV files
rm outputs/csv/*_2025-11_*.csv
```

---

## 🎯 Best Practices

### 1. **Module Structure**

```
✅ Good:
my_feature/
├── __init__.py
├── core.py          # Main logic
├── tools.py         # @tool decorated functions
├── config.py        # Configuration
└── tests.py         # Unit tests

❌ Bad:
all_in_one.py       # Everything mixed together
```

### 2. **Naming Conventions**

```
✅ Tools:
- search_options
- batch_search_options
- make_option_table
- analyze_options_chain

✅ Modules:
- options_search.py
- csv_export.py
- performance_monitor.py

❌ Bad:
- s1.py, t2.py
- my_tool, function1
- analyze (too generic)
```

### 3. **Documentation**

Every new file should have:

```python
"""
Module Description
Author: Name
Purpose: Clear statement of purpose

Key Functions:
- function_1: What it does
- function_2: What it does
"""
```

### 4. **Configuration Access**

✅ **Good**: Centralized settings
```python
from config.settings import LIMITS, PATHS

limit = LIMITS.MAX_OPTIONS_CONTRACTS
csv_dir = PATHS.CSV_DIR
```

❌ **Bad**: Hardcoded values
```python
limit = 1000
csv_dir = "outputs/csv"
```

### 5. **Error Handling**

✅ **Good**: Meaningful messages
```python
if not api_key:
    raise ValueError(
        "POLYGON_API_KEY missing. "
        "Set it in .env file."
    )
```

❌ **Bad**: Generic errors
```python
if not api_key:
    raise Exception("Error")
```

### 6. **File Organization**

✅ **Good**: Logical grouping
```
tools/
├── search/      # All search-related
├── export/      # All export formats
└── analysis/    # All analysis functions
```

❌ **Bad**: Random placement
```
tools/
├── search_options.py
├── plot_chart.py
├── csv_export.py
├── analyze.py
└── batch_search.py
```

---

## 📝 Adding New Features

### Complete Example: Adding a New Analysis Tool

**Step 1: Create file**
```bash
touch tools/analysis/new_metric.py
```

**Step 2: Implement tool**
```python
# tools/analysis/new_metric.py
"""
New Metric Analysis Tool
Author: You
Purpose: Calculate custom metrics
"""

from langchain_core.tools import tool
from config.settings import LIMITS

@tool
def calculate_new_metric(ticker: str, data: str) -> str:
    """
    Calculate new metric on options data.
    
    Args:
        ticker: Stock symbol (FIRST parameter!)
        data: JSON options data
    
    Returns:
        JSON with metric results
    """
    # Implementation
    return json.dumps(result)
```

**Step 3: Register in agent**
```python
# In agent_main.py or tools/analysis/__init__.py

from tools.analysis.new_metric import calculate_new_metric

analysis_tools = [
    # ... existing tools ...
    calculate_new_metric,  # Add here
]
```

**Step 4: Update documentation**
```bash
# Add to API_REFERENCE.md
## `calculate_new_metric()`
Description and usage...
```

**Step 5: Test**
```python
# Run agent
python agent_main.py

# Try using it
User: Use the new metric to analyze AAPL options
```

---

## 🔄 Refactoring Checklist

When refactoring or reorganizing:

- [ ] All imports updated
- [ ] Configuration centralized (no hardcoded values)
- [ ] Tool decorators applied (@tool)
- [ ] Documentation updated
- [ ] Tests passing
- [ ] No circular dependencies
- [ ] Error handling added
- [ ] Type hints included
- [ ] Configuration classes extended if needed
- [ ] Git commits with clear messages

---

## 📊 Organization Statistics

| Category | Files | Purpose |
|----------|-------|---------|
| **Tools** | 10+ | Agent capabilities |
| **Config** | 2 | Settings management |
| **RAG** | 4 | Knowledge base |
| **Evaluation** | 4 | Quality assurance |
| **Monitoring** | 1 | Performance tracking |
| **Documentation** | 6 | User guides |
| **Data Storage** | 3+ | Persistence |
| **Examples** | 6+ | Learning |

---

## 🎓 Learning Path

To understand the codebase:

1. **Week 1** (`Week1/`)
   - Basic LangGraph concepts
   - Tool integration
   - Memory management

2. **Configuration** (`config/settings.py`)
   - How settings are managed
   - How to add new config

3. **Tools** (`tools/`)
   - Tool structure and @tool decorator
   - How tools are composed
   - How to add new tools

4. **RAG** (`rag/`)
   - Knowledge base architecture
   - Vector vs. structured storage
   - How to use RAG

5. **Agent** (`agent_main.py`)
   - Complete system assembly
   - Graph construction
   - Execution flow

6. **Evaluation** (`evaluation/`)
   - Testing framework
   - Metrics collection
   - A/B testing

---

## 🚀 Deployment Considerations

### For Production:

1. **Environment**
   - Set all required API keys
   - Configure HTTPS
   - Set DEBUG=False

2. **Database**
   - Regular backups
   - Performance tuning
   - Data retention policy

3. **Scaling**
   - Use microservice API
   - Implement rate limiting
   - Monitor resource usage

4. **Security**
   - Never commit API keys
   - Use environment variables
   - Implement input validation
   - Add authentication

---

## 📚 Additional Resources

- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0  
**Maintainer**: Leo Ji

