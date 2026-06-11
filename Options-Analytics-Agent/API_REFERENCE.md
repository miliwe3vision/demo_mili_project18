# API Reference

Complete documentation of all tools and functions available in the Financial Options Analysis Agent.

---

## 🎯 Tool Categories

1. **Search Tools** - Get options data
2. **Export Tools** - Convert to CSV/Charts
3. **Analysis Tools** - Professional analysis
4. **RAG Tools** - Knowledge base access
5. **Utility Tools** - Helper functions

---

## 🔍 Search Tools

### `search_options()`

Search for options data for a single stock ticker with smart caching.

**Signature:**
```python
@tool
def search_options(
    ticker: str,
    date: str,
    limit: int = 300,
    force_refresh: bool = False
) -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker` | string | Yes | - | Stock symbol (e.g., "AAPL", "TSLA") |
| `date` | string | Yes | - | YYYY-MM-DD or YYYY-MM format |
| `limit` | integer | No | 300 | Max contracts to return (1-1000) |
| `force_refresh` | boolean | No | False | Skip cache if True |

**Returns:**
- JSON string with options data
- Contains: expiration_date, strike_price, type (call/put), bid, ask, volume, etc.

**Examples:**

```python
# Get 100 AAPL options expiring on December 19, 2025
search_options("AAPL", "2025-12-19", limit=100)

# Get all October 2025 TSLA options
search_options("TSLA", "2025-10", limit=500)

# Force refresh (skip cache)
search_options("MSFT", "2025-12-19", force_refresh=True)
```

**Caching Behavior:**
- **Default** (`force_refresh=False`): Checks knowledge base first
  - If found: Returns cached data instantly ⚡
  - If not found: Fetches from API and caches result
- **Forced** (`force_refresh=True`): Always fetches fresh data from API

---

### `batch_search_options()`

Efficiently search options for multiple stock tickers simultaneously.

**Signature:**
```python
@tool
def batch_search_options(
    tickers: list[str],
    date: str,
    limit: int = 100
) -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `tickers` | list | Yes | - | List of stock symbols (e.g., ["AAPL", "TSLA"]) |
| `date` | string | Yes | - | YYYY-MM-DD or YYYY-MM format (same for all) |
| `limit` | integer | No | 100 | Max contracts per ticker (1-1000) |

**Returns:**
- JSON string with dictionary of results
- Key: ticker symbol, Value: options data

**Examples:**

```python
# Get options for 3 stocks on same date
batch_search_options(
    ["AAPL", "TSLA", "MSFT"],
    "2025-12-19",
    limit=200
)

# Get monthly options for multiple stocks
batch_search_options(
    ["NVDA", "AMD", "INTEL"],
    "2025-12",
    limit=300
)
```

**Benefits:**
- Single API call for multiple tickers
- Parallel processing
- More efficient than individual searches
- Better for comparative analysis

---

## 📤 Export Tools

### `make_option_table()`

Convert options data to CSV format and save to file.

**Signature:**
```python
@tool
def make_option_table(
    data: str,
    ticker: str
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | string | Yes | JSON string from search_options |
| `ticker` | string | Yes | Stock symbol (for filename) |

**Returns:**
- Success message with filename
- File saved to: `outputs/csv/[TICKER]_options_[DATE]_[TIMESTAMP].csv`

**CSV Columns:**

| Column | Type | Description |
|--------|------|-------------|
| `expiration_date` | date | Options expiration date |
| `strike_price` | float | Strike price |
| `contract_type` | string | "call" or "put" |
| `bid_price` | float | Current bid price |
| `ask_price` | float | Current ask price |
| `implied_volatility` | float | IV as percentage |
| `delta` | float | Delta Greek |
| `gamma` | float | Gamma Greek |
| `theta` | float | Theta Greek |
| `vega` | float | Vega Greek |
| `open_interest` | integer | Open interest count |
| `volume` | integer | Daily volume |

**Examples:**

```python
# Export data from previous search
make_option_table(
    data='{"results": [...]}',
    ticker="AAPL"
)

# Typical workflow
# 1. search_options("AAPL", "2025-12-19", limit=200) -> returns data
# 2. make_option_table(data, "AAPL") -> saves CSV
```

**Output Example:**
```
✅ Exported: outputs/csv/AAPL_options_2025-12_20251215_143022.csv
   - 200 contracts
   - Ready for analysis or import
```

---

### `plot_options_chain()`

Generate PNG chart visualization of options data.

**Signature:**
```python
@tool
def plot_options_chain(
    data: str,
    ticker: str
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `data` | string | Yes | JSON string from search_options |
| `ticker` | string | Yes | Stock symbol (for chart title) |

**Returns:**
- Success message with filename
- File saved to: `outputs/charts/[TICKER]_options_[DATE]_[TIMESTAMP].png`

**Chart Types Generated:**

1. **Strike vs Implied Volatility**
   - Scatter plot: shows IV curve
   - Helps identify smile/skew

2. **Call vs Put Volume**
   - Bar chart: call/put comparison
   - Shows market sentiment

3. **Price Range Distribution**
   - Histogram: strike price density
   - Shows concentration

**Examples:**

```python
# Generate chart from search data
plot_options_chain(
    data='{"results": [...]}',
    ticker="TSLA"
)

# Creates professional-grade visualization
# - High resolution (100 DPI)
# - Labeled axes and legend
# - Color-coded calls (green) and puts (red)
```

**Output Example:**
```
✅ Chart generated: outputs/charts/TSLA_options_2025-12.png
   - Shows 200 contracts
   - Ready for presentation or analysis
```

---

## 📊 Analysis Tools

### `analyze_options_chain()`

Perform comprehensive professional analysis on options data.

**Signature:**
```python
@tool
def analyze_options_chain(
    ticker: str,
    options_data: str
) -> str
```

**⚠️ Critical:** Ticker must be FIRST parameter!

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Stock symbol (FIRST parameter!) |
| `options_data` | string | Yes | JSON string from search_options |

**Analysis Components:**

1. **Greeks Analysis**
   - Delta: Directional exposure
   - Gamma: Delta acceleration
   - Theta: Time decay
   - Vega: Volatility sensitivity

2. **Chain Metrics**
   - Call/Put ratio
   - Volume-weighted metrics
   - Open interest patterns
   - Implied volatility skew

3. **Sentiment Indicators**
   - Bullish/bearish positioning
   - Expected move calculation
   - Support/resistance levels

4. **Risk Assessment**
   - Concentration risk
   - Liquidity analysis
   - Greeks distribution

**Returns:**
- Comprehensive analysis report as string
- Professional interpretation and insights

**Examples:**

```python
# First get data
options_data = search_options("AAPL", "2025-12-19", limit=300)

# Then analyze (ticker FIRST!)
analyze_options_chain("AAPL", options_data)
```

**Output Sections:**

```
📊 COMPREHENSIVE OPTIONS ANALYSIS FOR AAPL
═══════════════════════════════════════════

1. CHAIN OVERVIEW
   - Total contracts: 300
   - Calls: 150, Puts: 150
   - Date range: [details]

2. GREEKS ANALYSIS
   - Average delta: [value]
   - Total gamma: [value]
   - [more metrics]

3. VOLATILITY ANALYSIS
   - IV range: [min-max]
   - Implied move: [±percentage]
   - Skew pattern: [shape]

4. SENTIMENT INDICATORS
   - Overall sentiment: [bullish/neutral/bearish]
   - Confidence score: [0-100]
   - Key levels: [support/resistance]

5. LIQUIDITY ASSESSMENT
   - High liquidity zones: [strike ranges]
   - Wide bid-ask spreads: [warnings]
```

---

### `quick_sentiment_check()`

Fast sentiment assessment without full analysis.

**Signature:**
```python
@tool
def quick_sentiment_check(
    ticker: str,
    options_data: str
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Stock symbol (FIRST parameter!) |
| `options_data` | string | Yes | JSON from search_options |

**Returns:**
- Quick sentiment verdict: Bullish/Neutral/Bearish
- Confidence score (0-100)
- Key reason for assessment

**Speed:** Much faster than full analysis (< 1 second)

**Examples:**

```python
# Quick check without full analysis
quick_sentiment_check("TSLA", options_data)

# Use for rapid screening across multiple stocks
for ticker in ["AAPL", "MSFT", "GOOGL"]:
    data = search_options(ticker, "2025-12-19", limit=100)
    quick_sentiment_check(ticker, data)
```

---

### `compare_options_sentiment()`

Compare options sentiment between two stocks.

**Signature:**
```python
@tool
def compare_options_sentiment(
    ticker1: str,
    data1: str,
    ticker2: str,
    data2: str
) -> str
```

**⚠️ Critical:** Ticker symbols must be FIRST parameters!

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker1` | string | Yes | First stock symbol |
| `data1` | string | Yes | Options data for ticker1 |
| `ticker2` | string | Yes | Second stock symbol |
| `data2` | string | Yes | Options data for ticker2 |

**Returns:**
- Side-by-side sentiment comparison
- Relative positioning analysis
- Investment implications

**Examples:**

```python
# Compare sentiment between two competitors
data_aapl = search_options("AAPL", "2025-12-19", limit=200)
data_msft = search_options("MSFT", "2025-12-19", limit=200)

compare_options_sentiment("AAPL", data_aapl, "MSFT", data_msft)
```

**Output Format:**

```
📊 COMPARATIVE SENTIMENT ANALYSIS
══════════════════════════════════

AAPL vs MSFT - December 19, 2025

┌─────────┬────────┬────────┐
│ Metric  │  AAPL  │  MSFT  │
├─────────┼────────┼────────┤
│Sentiment│Bullish │Neutral │
│ Score   │  75/100│  55/100│
│Call/Put │  1.2   │  0.9   │
│IV Skew  │Slight  │  Neutral│
└─────────┴────────┴────────┘

WINNER: AAPL shows stronger bullish positioning
```

---

### `generate_options_report()`

Create professional report in various formats.

**Signature:**
```python
@tool
def generate_options_report(
    ticker: str,
    format_type: str
) -> str
```

**Parameters:**

| Parameter | Type | Required | Options | Description |
|-----------|------|----------|---------|-------------|
| `ticker` | string | Yes | - | Stock symbol |
| `format_type` | string | Yes | 'full', 'summary', 'json' | Report format |

**Format Types:**

1. **'full'** - Comprehensive report
   - All analysis sections
   - Historical context
   - Recommendations
   - Professional formatting

2. **'summary'** - Executive summary
   - Key metrics only
   - Quick insights
   - Suitable for presentations

3. **'json'** - Machine-readable format
   - All metrics in JSON
   - For data integration
   - Easy parsing

**Examples:**

```python
# Full professional report
generate_options_report("AAPL", "full")

# Quick summary for presentation
generate_options_report("TSLA", "summary")

# JSON for system integration
generate_options_report("MSFT", "json")
```

---

## 📚 RAG (Knowledge Base) Tools

### Collection Tools

#### `collect_and_store_options()`

Search and immediately store options data in knowledge base.

**Signature:**
```python
@tool
def collect_and_store_options(
    ticker: str,
    date: str,
    limit: int
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Stock symbol |
| `date` | string | Yes | YYYY-MM-DD or YYYY-MM |
| `limit` | integer | Yes | Number of contracts (300-500 recommended) |

**Returns:**
- Confirmation message with storage details
- Data now searchable in knowledge base

**Examples:**

```python
# Collect and store AAPL options
collect_and_store_options("AAPL", "2025-12-19", limit=400)

# Now this data is searchable and available for anomaly detection
```

---

#### `batch_collect_options()`

Collect and store options for multiple tickers simultaneously.

**Signature:**
```python
@tool
def batch_collect_options(
    tickers: list[str],
    date: str,
    limit: int
) -> str
```

**Examples:**

```python
# Efficiently collect multiple stocks
batch_collect_options(
    ["AAPL", "TSLA", "MSFT"],
    "2025-12-19",
    limit=350
)
```

---

#### `collect_date_range()`

Collect options across multiple months (historical data).

**Signature:**
```python
@tool
def collect_date_range(
    ticker: str,
    start_date: str,
    end_date: str,
    limit: int
) -> str
```

**Parameters:**

| Parameter | Type | Required | Format | Description |
|-----------|------|----------|--------|-------------|
| `ticker` | string | Yes | - | Stock symbol |
| `start_date` | string | Yes | YYYY-MM-DD | Start date (inclusive) |
| `end_date` | string | Yes | YYYY-MM-DD | End date (inclusive) |
| `limit` | integer | Yes | - | Contracts per date |

**Examples:**

```python
# Collect all December 2025 options for AAPL
collect_date_range(
    "AAPL",
    "2025-12-01",
    "2025-12-31",
    limit=300
)

# Creates historical snapshot for analysis
```

---

### Query Tools

#### `search_knowledge_base()`

Query knowledge base using natural language.

**Signature:**
```python
@tool
def search_knowledge_base(
    query: str,
    limit: int = 5
) -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Natural language query |
| `limit` | integer | No | 5 | Max results |

**Examples:**

```python
# Natural language queries
search_knowledge_base("AAPL options with high IV", limit=10)
search_knowledge_base("ATM calls expiring in January", limit=5)
search_knowledge_base("Tech stocks unusual volume", limit=3)
```

**How It Works:**
1. Converts query to embedding (semantic meaning)
2. Searches ChromaDB for similar snapshots
3. Returns most relevant historical data

---

#### `get_historical_options()`

Retrieve stored options data by date range.

**Signature:**
```python
@tool
def get_historical_options(
    ticker: str,
    start_date: str,
    end_date: str
) -> str
```

**Examples:**

```python
# Get all stored AAPL data from December
get_historical_options("AAPL", "2025-12-01", "2025-12-31")

# Compare across months
get_historical_options("TSLA", "2025-11-01", "2025-12-31")
```

---

#### `get_snapshot_by_id()`

Retrieve specific stored snapshot by ID.

**Signature:**
```python
@tool
def get_snapshot_by_id(snapshot_id: str) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `snapshot_id` | string | Yes | Unique snapshot identifier |

---

#### `detect_anomaly()`

Find unusual changes in options data using vector similarity.

**Signature:**
```python
@tool
def detect_anomaly(
    ticker: str,
    current_data: str
) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `ticker` | string | Yes | Stock symbol |
| `current_data` | string | Yes | Current options data |

**How It Works:**
1. Compares current data to historical snapshots
2. Uses vector similarity (embeddings)
3. Identifies unusual patterns
4. Flags potential anomalies

**Examples:**

```python
# Check for anomalies in current AAPL data
current_data = search_options("AAPL", "2025-12-19", limit=300)
detect_anomaly("AAPL", current_data)

# Output: Reports if anything unusual detected
```

---

## 🛠️ Utility Tools

### `code_execution_tool()`

Execute custom Python code for advanced analysis.

**Signature:**
```python
@tool
def code_execution_tool(code: str) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `code` | string | Yes | Python code to execute |

**Available Libraries:**
- numpy, pandas - Data manipulation
- scipy - Scientific computing
- matplotlib - Plotting
- json - Data parsing
- datetime - Date handling
- statistics - Statistical functions

**Examples:**

```python
# Calculate custom metrics
code_execution_tool("""
import numpy as np
prices = [100, 102, 101, 103]
returns = np.diff(prices) / prices[:-1]
volatility = np.std(returns)
print(f"Volatility: {volatility:.2%}")
""")

# Advanced analysis
code_execution_tool("""
import pandas as pd
# Create dataframe from options data
df = pd.DataFrame(results)
# Calculate statistics
stats = df.groupby('strike_price')['volume'].sum()
print(stats)
""")
```

---

### `get_performance_stats()`

Retrieve system performance metrics.

**Signature:**
```python
@tool
def get_performance_stats(mode: str = "current") -> str
```

**Parameters:**

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `mode` | string | No | "current" | "current", "summary", "history" |

**Modes:**

1. **"current"** - Last query stats
   - Tokens used
   - Tools called
   - Execution time
   - Cache hits

2. **"summary"** - Overall statistics
   - Total queries
   - Average performance
   - Most used tools
   - Token efficiency

3. **"history"** - Recent query history
   - Last 10-20 queries
   - Performance trends
   - Tool usage patterns

**Examples:**

```python
# Check last query performance
get_performance_stats("current")

# View overall performance
get_performance_stats("summary")

# See recent trends
get_performance_stats("history")
```

---

### `human_assistance()`

Request human input for decisions or clarifications.

**Signature:**
```python
@tool
def human_assistance(question: str) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | Question for human |

**Examples:**

```python
# Clarify ambiguous requests
human_assistance("Multiple tickers provided. Which should I prioritize?")

# Get approval for decisions
human_assistance("Export will create large file (500MB). Proceed?")
```

---

### `toolTavilySearch()`

Search the web for financial context.

**Signature:**
```python
@tool
def toolTavilySearch(query: str) -> str
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |

**Examples:**

```python
# Get company context
toolTavilySearch("Apple Inc latest earnings report")

# Find ticker symbols
toolTavilySearch("Tesla TSLA current stock price")

# Get market news
toolTavilySearch("Tech sector volatility spike December 2025")
```

---

## 📋 Complete Workflow Examples

### Example 1: Basic Search and Export

```
User: Get options for AAPL on 2025-12-19 and save to CSV

Flow:
1. search_options("AAPL", "2025-12-19", limit=300)
   → Returns JSON with options data
2. make_option_table(data, "AAPL")
   → Saves CSV file
3. Agent responds: "✅ Exported to outputs/csv/AAPL_options_*.csv"
```

### Example 2: Analysis Workflow

```
User: Analyze TSLA options for December 19

Flow:
1. search_options("TSLA", "2025-12-19", limit=400)
2. analyze_options_chain("TSLA", data)
3. Agent provides comprehensive analysis report
```

### Example 3: Comparative Analysis

```
User: Compare AAPL and MSFT options sentiment

Flow:
1. search_options("AAPL", "2025-12-19", limit=200)
2. search_options("MSFT", "2025-12-19", limit=200)
3. compare_options_sentiment("AAPL", data1, "MSFT", data2)
4. Receive detailed comparison
```

### Example 4: Historical Anomaly Detection

```
User: Detect anomalies in NVDA options

Flow:
1. collect_date_range("NVDA", "2025-12-01", "2025-12-31", limit=300)
   → Build knowledge base
2. Get latest: search_options("NVDA", "2025-12-19", limit=300)
3. detect_anomaly("NVDA", current_data)
4. Receive anomaly report
```

---

## 🔄 Data Flow Reference

```
┌──────────────────────────────────────────────────────┐
│              TOOL EXECUTION FLOW                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  search_options() ──────┐                           │
│         ↓               ├─→ options data (JSON)    │
│  batch_search_options()─┘                          │
│                                                      │
│  options data (JSON)                                │
│         ↓                                            │
│    ┌────┴────────────────────┐                     │
│    ↓                         ↓                      │
│  make_option_table()   plot_options_chain()        │
│    ↓                         ↓                      │
│  CSV file              PNG chart                    │
│                                                      │
│  options data (JSON)                                │
│         ↓                                            │
│    ┌────┴─────────────────────────────┐            │
│    ↓         ↓          ↓          ↓               │
│ analyze_  quick_   compare_  generate_            │
│ options_  sentiment sentiment  options_           │
│ chain    check    comparison   report             │
│         Analysis reports                           │
│                                                      │
│  collect_and_store_options()                       │
│         ↓                                            │
│  Knowledge Base                                     │
│         ↓                                            │
│  ┌─→ search_knowledge_base()                       │
│  ├─→ get_historical_options()                      │
│  ├─→ get_snapshot_by_id()                          │
│  └─→ detect_anomaly()                              │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## ⚙️ Error Handling

All tools return string responses. Check for:

```python
# Success response
"✅ Exported to outputs/csv/..."

# Error response
"❌ Error: [reason]"

# Warning
"⚠️ [warning message]"
```

---

## 🚀 Performance Tips

1. **Use caching**: Default behavior checks knowledge base first
2. **Batch operations**: Use `batch_search_options()` for multiple tickers
3. **Limit results**: Start with smaller limits (100-200), increase as needed
4. **Reuse data**: Store once, query multiple times with `search_knowledge_base()`

---

**Last Updated**: December 15, 2025  
**Version**: 1.0.0

