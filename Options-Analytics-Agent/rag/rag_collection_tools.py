"""
RAG Data Collection Tools
主动数据采集工具：让AI自动收集和存储期权数据
"""
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict
from langchain_core.tools import tool

# 导入核心功能
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

@tool
def collect_and_store_options(
    ticker: str,
    date: str,
    limit: int = 500,
    force_update: bool = False
) -> str:
    """Automatically collect options data and store it in the knowledge base.
    
    This tool combines search_options and store_options_data into one step.
    It will check if data already exists before collecting new data.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        date: Date or month (e.g., '2025-11' or '2025-11-07')
        limit: Number of contracts to collect (default: 500)
        force_update: If True, collect even if data exists (default: False)
    
    Returns:
        Status message with collection and storage details
    
    Example:
        collect_and_store_options("AAPL", "2025-11", 500)
    """
    # 延迟导入，避免循环导入
    from search_tools import search_options
    from rag_tools import store_options_data
    from rag_knowledge_base import query_sqlite
    
    try:
        print(f"\n🤖 Auto-collecting data for {ticker} {date}...")
        
        # 检查是否已存在
        if not force_update:
            existing = query_sqlite(ticker=ticker, start_date=date, end_date=date, limit=1)
            if existing:
                return f"""ℹ️ Data already exists for {ticker} {date}
                
📊 Existing snapshot:
  • ID: {existing[0]['id']}
  • Contracts: {existing[0]['total_contracts']}
  • Captured: {existing[0]['timestamp']}
  
💡 Use force_update=True to refresh the data."""
        
        # 1. 采集数据
        print(f"📡 Collecting options data...")
        data = search_options.invoke({"ticker": ticker, "date": date, "limit": limit})
        
        # 验证数据
        options_data = json.loads(data)
        if "error" in options_data:
            return f"❌ Error collecting data: {options_data['error']}"
        
        count = options_data.get("count", 0)
        if count == 0:
            return f"⚠️ No options data found for {ticker} {date}"
        
        print(f"✅ Collected {count} contracts")
        
        # 2. 存储到知识库
        print(f"💾 Storing to knowledge base...")
        storage_result = store_options_data.invoke({"data": data, "ticker": ticker, "date": date})
        
        # 3. 格式化结果
        result = f"""🤖 Auto-Collection Complete!

📡 Collection:
  • Ticker: {ticker}
  • Date: {date}
  • Contracts Collected: {count}
  • Data Source: Polygon.io

💾 Storage:
{storage_result}

✅ Data is now available in the knowledge base!
"""
        return result
        
    except Exception as e:
        return f"❌ Error in auto-collection: {str(e)}"


@tool
def batch_collect_options(
    tickers: str,
    date: str,
    limit: int = 300
) -> str:
    """Collect and store options data for multiple tickers at once.
    
    This tool allows efficient batch collection of data for multiple stocks.
    
    Args:
        tickers: Comma-separated ticker symbols (e.g., 'AAPL,TSLA,MSFT')
        date: Date or month for all tickers
        limit: Number of contracts per ticker
    
    Returns:
        Summary of batch collection results
    
    Example:
        batch_collect_options("AAPL,TSLA,MSFT", "2025-11", 300)
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]
        
        print(f"\n🚀 Batch collection for {len(ticker_list)} tickers...")
        
        results = []
        successful = 0
        failed = 0
        
        for i, ticker in enumerate(ticker_list, 1):
            print(f"\n[{i}/{len(ticker_list)}] Processing {ticker}...")
            
            result = collect_and_store_options.invoke({"ticker": ticker, "date": date, "limit": limit})
            
            if "❌" in result or "Error" in result:
                failed += 1
                status = "❌ Failed"
            else:
                successful += 1
                status = "✅ Success"
            
            results.append(f"{status} {ticker}")
            
            # 避免API限流，稍作延迟
            if i < len(ticker_list):
                time.sleep(1)
        
        # 生成摘要
        summary = f"""🚀 Batch Collection Complete!

📊 Summary:
  • Total Tickers: {len(ticker_list)}
  • Successful: {successful}
  • Failed: {failed}
  • Date: {date}

📋 Details:
"""
        for result in results:
            summary += f"  {result}\n"
        
        return summary
        
    except Exception as e:
        return f"❌ Error in batch collection: {str(e)}"


@tool
def collect_date_range(
    ticker: str,
    start_date: str,
    end_date: str,
    limit: int = 300
) -> str:
    """Collect options data for a ticker across multiple dates.
    
    This tool collects data for all expiration dates in a given range.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date (YYYY-MM-DD or YYYY-MM)
        end_date: End date (YYYY-MM-DD or YYYY-MM)
        limit: Contracts per date
    
    Returns:
        Summary of date range collection
    
    Example:
        collect_date_range("AAPL", "2025-11", "2026-01", 300)
    """
    
    try:
        print(f"\n📅 Collecting date range for {ticker}: {start_date} to {end_date}...")
        
        # 生成日期列表（按月）
        dates = []
        
        # 简单实现：如果是月份格式
        if len(start_date) == 7:  # YYYY-MM
            start = datetime.strptime(start_date, "%Y-%m")
            end = datetime.strptime(end_date, "%Y-%m")
            
            current = start
            while current <= end:
                dates.append(current.strftime("%Y-%m"))
                # 下一个月
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
        else:
            return "⚠️ Please use YYYY-MM format for date range collection"
        
        print(f"📊 Will collect {len(dates)} months of data")
        
        results = []
        successful = 0
        failed = 0
        
        for i, date in enumerate(dates, 1):
            print(f"\n[{i}/{len(dates)}] Collecting {ticker} {date}...")
            
            result = collect_and_store_options.invoke({"ticker": ticker, "date": date, "limit": limit})
            
            if "❌" in result or "Error" in result:
                failed += 1
                status = "❌"
            else:
                successful += 1
                status = "✅"
            
            results.append(f"{status} {date}")
            
            # 延迟避免API限流
            if i < len(dates):
                time.sleep(2)
        
        summary = f"""📅 Date Range Collection Complete!

📊 Summary:
  • Ticker: {ticker}
  • Date Range: {start_date} to {end_date}
  • Total Months: {len(dates)}
  • Successful: {successful}
  • Failed: {failed}

📋 Details:
"""
        for result in results:
            summary += f"  {result}\n"
        
        return summary
        
    except Exception as e:
        return f"❌ Error in date range collection: {str(e)}"


@tool
def check_missing_data(ticker: str, months_back: int = 3) -> str:
    """Check what data is missing from the knowledge base.
    
    This tool helps identify gaps in your data collection.
    
    Args:
        ticker: Stock ticker to check
        months_back: How many months back to check (default: 3)
    
    Returns:
        Report of missing data
    
    Example:
        check_missing_data("AAPL", 6)
    """
    # 延迟导入
    from rag_knowledge_base import query_sqlite
    
    try:
        print(f"\n🔍 Checking missing data for {ticker}...")
        
        # 生成应该有的月份列表
        expected_dates = []
        current_date = datetime.now()
        
        for i in range(months_back):
            date = current_date - timedelta(days=30 * i)
            expected_dates.append(date.strftime("%Y-%m"))
        
        # 检查哪些已存在
        existing = query_sqlite(ticker=ticker, limit=100)
        existing_dates = set([e['date'][:7] for e in existing])  # 取 YYYY-MM
        
        # 找出缺失的
        missing = [d for d in expected_dates if d not in existing_dates]
        
        report = f"""🔍 Data Coverage Report for {ticker}

📊 Analysis:
  • Period: Last {months_back} months
  • Expected: {len(expected_dates)} months
  • Found: {len(existing_dates)} months
  • Missing: {len(missing)} months

"""
        
        if missing:
            report += "⚠️ Missing Data:\n"
            for date in missing:
                report += f"  • {date}\n"
            report += f"\n💡 To collect missing data, use:\n"
            for date in missing[:3]:  # 只显示前3个
                report += f"  collect_and_store_options('{ticker}', '{date}', 300)\n"
        else:
            report += "✅ All data is up to date!\n"
        
        if existing:
            report += f"\n📅 Latest snapshot: {existing[0]['date']}\n"
            report += f"   Captured: {existing[0]['timestamp']}\n"
        
        return report
        
    except Exception as e:
        return f"❌ Error checking missing data: {str(e)}"


@tool
def auto_update_watchlist(tickers: str, date: str = None) -> str:
    """Automatically update data for a watchlist of tickers.
    
    This is a convenience tool for regularly updating your tracked stocks.
    
    Args:
        tickers: Comma-separated ticker list (e.g., 'AAPL,TSLA,MSFT')
        date: Optional specific date (default: current month)
    
    Returns:
        Update summary
    
    Example:
        auto_update_watchlist("AAPL,TSLA,MSFT,NVDA")
    """
    
    try:
        # 如果没有指定日期，使用当前月
        if not date:
            date = datetime.now().strftime("%Y-%m")
        
        print(f"\n🔄 Updating watchlist for {date}...")
        
        result = batch_collect_options.invoke({"tickers": tickers, "date": date, "limit": 500})
        
        return f"""🔄 Watchlist Update Complete!

📅 Date: {date}
📊 Tickers: {tickers}

{result}

💡 Next update: Run this tool again next month!
"""
        
    except Exception as e:
        return f"❌ Error updating watchlist: {str(e)}"


# ==================== 工具列表 ====================

collection_tools = [
    collect_and_store_options,
    batch_collect_options,
    collect_date_range,
    check_missing_data,
    auto_update_watchlist
]

if __name__ == "__main__":
    print("RAG Collection Tools loaded:")
    for tool in collection_tools:
        print(f"  • {tool.name}")

