"""
Auralis-DSA: Optimized Market Session Analyzer & Trade Risk Engine
==================================================================
Course: CS-250 — Data Structures & Algorithms
Instructor: Dr. Ayesha Hakim

Main Driver - Demonstrates all three DSA modules:
1. CandleStore (Dynamic Array + Binary Search)
2. SessionManager (AVL Tree)
3. TradeManager (Linked List + Max-Heap)

This script loads real XAUUSD OHLC data and demonstrates each module's
functionality with actual market data.
"""

import sys
import io
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dsa.candle_store import CandleStore, Candle, DynamicArray
from dsa.session_manager import SessionManager, AVLTree
from dsa.trade_manager import TradeManager, Trade, LinkedList, MaxHeap
from data_loader import load_price_data


def print_header(title: str) -> None:
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_subheader(title: str) -> None:
    """Print formatted subsection header."""
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


def load_candles_from_dataframe(df: pd.DataFrame, limit: int = None) -> CandleStore:
    """
    Load candles from DataFrame into CandleStore.
    
    Args:
        df: DataFrame with OHLC data
        limit: Maximum number of candles to load (None for all)
    
    Returns:
        Populated CandleStore
    """
    store = CandleStore()
    
    # Find timestamp column
    ts_col = [c for c in df.columns if 'time' in c.lower()][0]
    
    count = 0
    for _, row in df.iterrows():
        if limit and count >= limit:
            break
        
        candle = Candle(
            timestamp=row[ts_col].to_pydatetime().replace(tzinfo=None),
            open_price=float(row['open']),
            high=float(row['high']),
            low=float(row['low']),
            close=float(row['close']),
            volume=float(row.get('volume', 0))
        )
        store.insert(candle)
        count += 1
    
    return store


def demo_module1_candle_store(df: pd.DataFrame) -> CandleStore:
    """
    Demonstrate Module 1: CandleStore (Dynamic Array + Binary Search)
    """
    print_header("MODULE 1: CandleStore (Dynamic Array + Binary Search)")
    
    print("\n📊 Loading XAUUSD M5 data into CandleStore...")
    store = load_candles_from_dataframe(df, limit=10000)
    
    stats = store.get_stats()
    print(f"\n✅ Data Loaded Successfully!")
    print(f"   • Candles stored: {stats['size']:,}")
    print(f"   • Array capacity: {stats['capacity']:,}")
    print(f"   • Array resizes (doubling): {stats['resize_count']}")
    print(f"   • Load factor: {stats['load_factor']:.2%}")
    
    # Demonstrate binary search
    print_subheader("Binary Search Performance")
    
    # Search for specific timestamps
    if len(store) > 0:
        # Get middle candle timestamp
        mid_idx = len(store) // 2
        target_ts = store[mid_idx].timestamp
        
        print(f"\n🔍 Searching for timestamp: {target_ts}")
        idx = store.binary_search_timestamp(target_ts)
        
        if idx >= 0:
            found = store[idx]
            print(f"   ✓ Found at index {idx}")
            print(f"   ✓ Candle: O={found.open:.2f}, H={found.high:.2f}, L={found.low:.2f}, C={found.close:.2f}")
            print(f"   ✓ Comparisons made: {store.last_comparisons}")
            print(f"   ✓ Expected O(log n) ≈ {len(bin(len(store))) - 2}")
    
    # Calculate Asia session range
    print_subheader("Session Range Calculation")
    
    if len(store) > 72:  # At least one day of M5 data
        sample_date = store[0].timestamp.replace(hour=0, minute=0, second=0)
        asia_high, asia_low = store.calculate_asia_range(sample_date)
        
        print(f"\n📈 Asian Session Range for {sample_date.date()}:")
        print(f"   • Asia High: ${asia_high:.2f}")
        print(f"   • Asia Low:  ${asia_low:.2f}")
        print(f"   • Range:     ${asia_high - asia_low:.2f}")
    
    return store


def demo_module2_session_manager() -> SessionManager:
    """
    Demonstrate Module 2: SessionManager (AVL Tree)
    """
    print_header("MODULE 2: SessionManager (AVL Tree)")
    
    manager = SessionManager(use_defaults=True)
    
    print("\n🌳 AVL Tree Structure:")
    print("   (Sessions stored as interval nodes)")
    print()
    manager.print_tree()
    
    stats = manager.get_stats()
    print(f"\n✅ Tree Statistics:")
    print(f"   • Number of sessions: {stats['size']}")
    print(f"   • Tree height: {stats['height']}")
    print(f"   • Rotations performed: {stats['total_rotations']}")
    print(f"   • Is balanced: {stats['is_balanced']}")
    
    print_subheader("Session Classification (O(log n) Lookup)")
    
    print("\n⏰ Classifying hours throughout the trading day:")
    print(f"   {'Hour (UTC)':<12} {'Session':<15} {'Comparisons'}")
    print(f"   {'-' * 12} {'-' * 15} {'-' * 12}")
    
    for hour in range(0, 24, 3):
        test_ts = datetime(2024, 1, 15, hour, 30, 0)
        info = manager.get_session_info(test_ts)
        print(f"   {hour:02d}:30        {info['session']:<15} {info['comparisons']}")
    
    print_subheader("Trading Hours Filter")
    
    london_hours = ["London"]
    test_times = [
        datetime(2024, 1, 15, 3, 0),   # Asian
        datetime(2024, 1, 15, 8, 0),   # London
        datetime(2024, 1, 15, 14, 0),  # NY overlap
        datetime(2024, 1, 15, 22, 0),  # Off-hours
    ]
    
    print("\n🇬🇧 London Session Filter Check:")
    for ts in test_times:
        session = manager.classify_timestamp(ts)
        is_london = manager.is_trading_hours(ts, london_hours)
        status = "✓ ALLOW" if is_london else "✗ SKIP"
        print(f"   {ts.strftime('%H:%M')} UTC ({session:<10}) → {status}")
    
    return manager


def demo_module3_trade_manager() -> TradeManager:
    """
    Demonstrate Module 3: TradeManager (Linked List + Max-Heap)
    """
    print_header("MODULE 3: TradeManager (Linked List + Max-Heap)")
    
    manager = TradeManager(max_risk_budget=100.0, max_concurrent_trades=6)
    
    print(f"\n⚙️ Risk Engine Configuration:")
    print(f"   • Max risk budget: {manager._max_risk_budget}")
    print(f"   • Max concurrent trades: {manager._max_concurrent}")
    
    print_subheader("Adding Trades")
    
    # Create realistic XAUUSD trades
    trades_data = [
        # (symbol, direction, entry, stop_loss, take_profit, size, description)
        ("XAUUSD", "LONG", 1950.00, 1945.00, 1960.00, 1.0, "Conservative long"),
        ("XAUUSD", "SHORT", 1955.00, 1962.00, 1940.00, 2.0, "Aggressive short"),
        ("XAUUSD", "LONG", 1948.00, 1940.00, 1965.00, 1.5, "Wide stop long"),
        ("XAUUSD", "SHORT", 1952.00, 1956.00, 1944.00, 0.8, "Tight stop short"),
        ("XAUUSD", "LONG", 1945.00, 1930.00, 1980.00, 3.0, "High risk position"),
        ("XAUUSD", "SHORT", 1960.00, 1965.00, 1950.00, 1.2, "Medium risk short"),
    ]
    
    print("\n📝 Inserting trades into LinkedList (O(1)) + MaxHeap (O(log n)):")
    for symbol, direction, entry, sl, tp, size, desc in trades_data:
        trade = manager.create_and_add_trade(symbol, direction, entry, sl, tp, size)
        print(f"   ✓ {desc}: Risk Score = {trade.risk_score:.2f}")
    
    stats = manager.get_stats()
    print(f"\n📊 Current Portfolio Status:")
    print(f"   • Active trades: {stats['active_trades']}")
    print(f"   • Total risk: {stats['total_risk']:.2f}")
    print(f"   • Risk utilization: {stats['risk_utilization']:.1%}")
    
    print_subheader("Risk-Based Prioritization (Max-Heap)")
    
    print("\n🔺 Trades sorted by risk (Heap extraction order):")
    print(f"   {'Rank':<6} {'Direction':<8} {'Entry':<10} {'Risk Score'}")
    print(f"   {'-' * 6} {'-' * 8} {'-' * 10} {'-' * 12}")
    
    # Get sorted without modifying
    trades_by_risk = manager.get_trades_by_risk()
    for i, trade in enumerate(trades_by_risk, 1):
        print(f"   {i:<6} {trade.direction:<8} ${trade.entry_price:<9.2f} {trade.risk_score:.2f}")
    
    print_subheader("Greedy Risk Enforcement Algorithm")
    
    print(f"\n⚠️ Reducing risk budget from 100.0 to 40.0...")
    manager._max_risk_budget = 40.0
    
    print(f"   Current total risk: {manager.total_risk:.2f}")
    print(f"   New budget: {manager._max_risk_budget:.2f}")
    print(f"\n   Enforcing risk limits (greedy removal of highest-risk trades)...")
    
    manager._enforce_risk_budget()
    
    stats = manager.get_stats()
    print(f"\n✅ After Risk Enforcement:")
    print(f"   • Active trades: {stats['active_trades']}")
    print(f"   • Total risk: {stats['total_risk']:.2f}")
    print(f"   • Trades removed: {stats['trades_removed_for_risk']}")
    
    print("\n📋 Remaining Trades (LinkedList traversal):")
    for trade in manager.get_all_trades():
        print(f"   • {trade.direction} @ ${trade.entry_price:.2f} (Risk: {trade.risk_score:.2f})")
    
    return manager


def demo_integrated_workflow(df: pd.DataFrame):
    """
    Demonstrate integrated workflow using all three modules together.
    """
    print_header("INTEGRATED WORKFLOW: All Modules Working Together")
    
    print("\n🔄 Simulating a trading workflow...")
    
    # 1. Load candles
    print("\n1️⃣ Loading market data into CandleStore...")
    store = load_candles_from_dataframe(df, limit=2000)
    print(f"   ✓ Loaded {len(store):,} candles")
    
    # 2. Initialize session manager
    print("\n2️⃣ Initializing SessionManager with AVL Tree...")
    session_mgr = SessionManager(use_defaults=True)
    print(f"   ✓ {len(session_mgr._tree)} trading sessions configured")
    
    # 3. Initialize trade manager
    print("\n3️⃣ Setting up TradeManager with risk limits...")
    trade_mgr = TradeManager(max_risk_budget=50.0, max_concurrent_trades=3)
    print(f"   ✓ Max risk: {trade_mgr._max_risk_budget}, Max trades: {trade_mgr._max_concurrent}")
    
    # 4. Simulate trading logic
    print("\n4️⃣ Simulating trade signals...")
    
    trades_taken = 0
    london_signals = 0
    
    for i in range(100, min(500, len(store))):
        candle = store[i]
        session = session_mgr.classify_timestamp(candle.timestamp)
        
        # Only trade during London session
        if session == "London":
            london_signals += 1
            
            # Simple signal: buy when close > open (bullish candle)
            if candle.close > candle.open and trades_taken < 5:
                entry = candle.close
                sl = candle.low - 1.0
                tp = entry + 2 * (entry - sl)  # 2R target
                
                trade = trade_mgr.create_and_add_trade(
                    "XAUUSD", "LONG", entry, sl, tp, 1.0
                )
                trades_taken += 1
                print(f"   📈 Trade #{trades_taken}: LONG @ ${entry:.2f} during {session} session")
    
    print(f"\n📊 Simulation Results:")
    print(f"   • Candles processed: 400")
    print(f"   • London session signals: {london_signals}")
    print(f"   • Trades taken: {trades_taken}")
    print(f"   • Final risk exposure: {trade_mgr.total_risk:.2f}")
    
    print("\n✅ All modules integrated successfully!")


def main():
    """Main entry point for Auralis-DSA demonstration."""
    try:
        print("\n" + "█" * 70)
        print("█" + " " * 68 + "█")
        print("█" + "  AURALIS-DSA: Optimized Market Session Analyzer".center(68) + "█")
        print("█" + "  & Trade Risk Engine".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" + "  CS-250 — Data Structures & Algorithms".center(68) + "█")
        print("█" + "  Instructor: Dr. Ayesha Hakim".center(68) + "█")
        print("█" + " " * 68 + "█")
        print("█" * 70)
    except UnicodeEncodeError:
        # Fallback for systems that don't support Unicode box characters
        print("\n" + "=" * 70)
        print("  AURALIS-DSA: Optimized Market Session Analyzer")
        print("  & Trade Risk Engine")
        print("  CS-250 — Data Structures & Algorithms")
        print("  Instructor: Dr. Ayesha Hakim")
        print("=" * 70)
    
    print("\n📚 Group Members:")
    print("   1. Muntazir Mehdi — CMS: 503710")
    print("   2. Muhammad Hannan Faisal — CMS: 507444")
    print("   3. Muhammad Sammar Abbas — CMS: 509701")
    
    # Load real market data
    print("\n" + "─" * 70)
    print("Loading XAUUSD market data...")
    try:
        df = load_price_data()
        print(f"✓ Loaded {len(df):,} candles from 2018-2025")
    except Exception as e:
        print(f"⚠️ Could not load real data: {e}")
        print("   Using synthetic data for demonstration...")
        df = None
    
    # Run demonstrations
    if df is not None:
        store = demo_module1_candle_store(df)
        session_mgr = demo_module2_session_manager()
        trade_mgr = demo_module3_trade_manager()
        demo_integrated_workflow(df)
    else:
        # Run with synthetic data
        from dsa.candle_store import demo_candle_store
        from dsa.session_manager import demo_session_manager
        from dsa.trade_manager import demo_trade_manager
        
        demo_candle_store()
        demo_session_manager()
        demo_trade_manager()
    
    print_header("DEMONSTRATION COMPLETE")
    print("\n✅ All three DSA modules demonstrated successfully!")
    print("\n📋 Summary of Data Structures & Algorithms Used:")
    print("   ┌─────────────────────────────────────────────────────────────┐")
    print("   │ Module 1: CandleStore                                       │")
    print("   │   • Dynamic Array (doubling strategy) - Amortized O(1)      │")
    print("   │   • Binary Search - O(log n)                                │")
    print("   ├─────────────────────────────────────────────────────────────┤")
    print("   │ Module 2: SessionManager                                    │")
    print("   │   • AVL Tree with rotations - O(log n) insert/search        │")
    print("   │   • In-order traversal - O(n)                               │")
    print("   ├─────────────────────────────────────────────────────────────┤")
    print("   │ Module 3: TradeManager                                      │")
    print("   │   • Doubly Linked List - O(1) insert/delete                 │")
    print("   │   • Max-Heap - O(log n) insert/extract                      │")
    print("   │   • Greedy algorithm for risk enforcement                   │")
    print("   └─────────────────────────────────────────────────────────────┘")
    
    print("\n🎯 Run 'python benchmark_dsa.py' for Big-O performance analysis.")


if __name__ == "__main__":
    main()

