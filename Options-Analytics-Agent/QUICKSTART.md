# Quick Start Guide

Get the Financial Options Analysis Agent up and running in 5 minutes.

---

## 🚀 30-Second Setup

### 1. Install Dependencies
```bash
cd /Users/leo/Desktop/CS\ projects/Algovant\ Internship
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Create .env file
cp .env.template .env  # If template exists, or create manually

# Edit .env with your API keys
nano .env
```

**Required API Keys:**
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- `POLYGON_API_KEY` - Get from https://polygon.io/dashboard/api-keys

**Optional:**
- `TAVILY_API_KEY` - Get from https://tavily.com
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com

### 3. Run Agent
```bash
python agent_main.py
```

That's it! You should see initialization messages.

---

## 💬 First Interaction

Once the agent is running, try these commands:

### Get Options Data
```
User: Get options for AAPL on 2025-12-19
```

### Export to CSV
```
User: Search options for TSLA on 2025-12-19, then export to CSV
```

### Generate Chart
```
User: Get 200 options for MSFT on 2025-12-19 and create a chart
```

### Analyze Options
```
User: Analyze the options for NVDA on 2025-12-19
```

### Search Multiple Tickers
```
User: Get options for AAPL, TSLA, and MSFT on 2025-12-19
```

---

## 🔧 Configuration (Optional)

### Change Default Model

Edit `config/settings.py`:

```python
class ModelConfig:
    MODEL_NAME = "gpt-4"  # Options: "gpt-4", "gpt-4-turbo", "gpt-4o-mini"
```

### Increase Context History

Edit `config/settings.py`:

```python
class Limits:
    MAX_MESSAGES = 50  # Default: 20
```

### Disable Performance Monitoring

Edit `config/settings.py`:

```python
class AgentConfig:
    ENABLE_PERFORMANCE_MONITORING = False
```

---

## 📊 Try These Use Cases

### 1. Weekly Options Analysis
```
User: Get options for my watchlist - AAPL, MSFT, GOOGL - 
      for all December 2025 dates, then export to CSV
```

### 2. Historical Anomaly Detection
```
User: Collect TSLA options from December 1-31, 2025
User: Detect any anomalies in this data
```

### 3. Custom Analysis
```
User: Search options for AMZN on 2025-12-19
User: Run custom analysis to find underpriced calls
```

### 4. Batch Export
```
User: Get 300 options each for AAPL and TSLA on 2025-12-19
      and create charts for both
```

---

## 🐛 Common Issues & Quick Fixes

### Issue: "API Key Not Found"
**Solution**:
```bash
# Verify .env exists in project root
ls -la .env

# Check it has content
cat .env

# Make sure file is readable
chmod 644 .env
```

### Issue: "Connection Refused"
**Solution**:
```bash
# Restart agent
Ctrl+C  # Stop current process
python agent_main.py  # Start fresh
```

### Issue: "Database Locked"
**Solution**:
```bash
# Clear database locks
rm -f data/conversation_memory.db-*

# Restart
python agent_main.py
```

### Issue: Slow Response
**Solutions**:
1. Use `force_refresh=False` (default - uses cache)
2. Reduce `MAX_MESSAGES` in config
3. Use smaller model (`gpt-4o-mini`)

---

## 🎓 Learning Resources

### For Beginners
Start with learning examples:
```bash
cd Week1
python first_simple_openai_agent.py
```

### For Intermediate Users
Study the main agent:
```bash
# Read the well-commented code
less agent_main.py

# Follow the initialization flow:
# 1. Configuration (settings.py)
# 2. Tools loading
# 3. LLM initialization
# 4. Graph building
# 5. Main loop
```

### For Advanced Users
Explore evaluation framework:
```bash
python run_evaluation.py
python run_ab_testing.py
python run_skills_ablation.py
```

---

## 🚀 Advanced: Run as Microservice

### Start FastAPI Server
```bash
cd microservice
python app.py

# Or with uvicorn
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Test Endpoints
```bash
# Search options
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "date": "2025-12-19",
    "limit": 100
  }'

# Export CSV
curl -X POST "http://localhost:8000/api/csv" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {...},
    "ticker": "AAPL"
  }'
```

### API Documentation
```
http://localhost:8000/docs
```

---

## 📁 Output Files

After running searches and exports, find results in:

```
outputs/
├── csv/                           # Exported CSV files
│   └── AAPL_options_2025-12_*.csv
│
└── charts/                        # Generated PNG charts
    └── AAPL_options_2025-12_*.png
```

---

## 💾 Conversation Memory

The agent remembers all conversations across sessions:

```bash
# View conversation history
sqlite3 data/conversation_memory.db "SELECT * FROM messages LIMIT 10;"

# Clear conversation history
python clear_memory.py

# Backup data
python backup.py
```

---

## 🔄 Using Rules-Based Agent

Alternative agent with external rule files:

```bash
python agent_with_rules.py
```

**Benefits:**
- Easier to update behavior
- Modular rule system
- Better maintainability

**Edit Rules:**
```
rules/agent_rules.md      # Core behaviors
rules/analysis_rules.md   # Analysis methodology
```

Rules automatically reload on agent restart.

---

## 🌟 Pro Tips

### 1. Use Keyboard Shortcuts
```
Ctrl+C        - Exit agent gracefully
Ctrl+D        - Also exits (EOF)
```

### 2. Smart Caching
```
# Uses cache by default (faster)
User: Get options for AAPL on 2025-12-19

# Force fresh data from API
User: Get options for AAPL on 2025-12-19 with force refresh
```

### 3. Batch Operations
```
# More efficient than individual searches
User: Get options for [AAPL, TSLA, MSFT] on 2025-12-19
```

### 4. Check Performance
```
User: Show me my performance statistics
```

### 5. Get Help
```
User: What tools do you have?
User: How do I use the chart generation?
User: Explain the analysis methodology
```

---

## 📈 Next Steps

1. **Explore Tools**
   - Try different export formats
   - Generate various chart types
   - Run analysis tools

2. **Build Knowledge Base**
   - Collect historical options data
   - Store snapshots for future reference
   - Use for anomaly detection

3. **Evaluate Performance**
   - Check performance statistics
   - Run A/B testing
   - Analyze skill importance

4. **Integrate & Scale**
   - Deploy microservice
   - Integrate with your systems
   - Build automation workflows

---

## 🆘 Need Help?

### Check Logs
```bash
# Run in debug mode
# Edit config/settings.py
class AgentConfig:
    DEBUG = True
    VERBOSE = True
```

### Review Documentation
- `README.md` - Full documentation
- `PROJECT_STRUCTURE.md` - File organization
- `rules/agent_rules.md` - Agent capabilities
- `Week1/README.md` - Learning materials

### Common Commands
```bash
# Check if setup is correct
python -c "from config.settings import settings; settings.initialize(); print('✅ Setup OK')"

# Test API connection
python -c "from config.settings import API_KEYS; API_KEYS.validate(); print('✅ API keys OK')"

# View current configuration
python -c "from config.settings import settings; print(settings.model.MODEL_NAME)"
```

---

## ✅ Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys configured (`.env` file)
- [ ] Agent starts successfully (`python agent_main.py`)
- [ ] Can search options (e.g., "AAPL 2025-12-19")
- [ ] Can export to CSV
- [ ] Can generate charts
- [ ] Performance stats available
- [ ] (Optional) Microservice runs (`python microservice/app.py`)

---

**Ready to go!** 🚀

Start with: `python agent_main.py`

---

**Quick Reference**:
- **Main Agent**: `python agent_main.py`
- **Rules Agent**: `python agent_with_rules.py`
- **API Server**: `python microservice/app.py`
- **Examples**: `python Week1/first_simple_openai_agent.py`
- **Full Docs**: Read `README.md`

---

*Last Updated: December 15, 2025*

