"""
Module 1: CandleStore (Dynamic Array + Binary Search)
=====================================================
Auralis-DSA: Optimized Market Session Analyzer & Trade Risk Engine
Course: CS-250 — Data Structures & Algorithms

Features:
- Custom DynamicArray class implementing doubling strategy
- Amortized O(1) insertions
- O(log n) manual binary search for timestamp lookup
- Efficient session range high/low calculations
"""

from datetime import datetime
from typing import Optional, List, Tuple, Any


class DynamicArray:
    """
    Custom Dynamic Array implementation with doubling strategy.
    
    Time Complexities:
    - Append: Amortized O(1)
    - Access by index: O(1)
    - Search (unsorted): O(n)
    - Binary Search (sorted): O(log n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, initial_capacity: int = 8):
        """Initialize dynamic array with given capacity."""
        self._capacity = initial_capacity
        self._size = 0
        self._data: List[Any] = [None] * self._capacity
        self._resize_count = 0  # Track number of resizes for analysis
    
    def _resize(self, new_capacity: int) -> None:
        """
        Resize internal array to new capacity.
        Time Complexity: O(n) - but amortized across insertions
        """
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
        self._resize_count += 1
    
    def append(self, element: Any) -> None:
        """
        Append element to end of array.
        Uses doubling strategy when capacity is reached.
        Time Complexity: Amortized O(1)
        """
        if self._size == self._capacity:
            # Double the capacity (doubling strategy)
            self._resize(self._capacity * 2)
        
        self._data[self._size] = element
        self._size += 1
    
    def __getitem__(self, index: int) -> Any:
        """
        Access element by index.
        Time Complexity: O(1)
        """
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")
        return self._data[index]
    
    def __setitem__(self, index: int, value: Any) -> None:
        """Set element at index. Time Complexity: O(1)"""
        if index < 0:
            index = self._size + index
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} out of range for size {self._size}")
        self._data[index] = value
    
    def __len__(self) -> int:
        """Return number of elements. Time Complexity: O(1)"""
        return self._size
    
    def __iter__(self):
        """Iterator for the array."""
        for i in range(self._size):
            yield self._data[i]
    
    @property
    def capacity(self) -> int:
        """Current capacity of internal array."""
        return self._capacity
    
    @property
    def resize_count(self) -> int:
        """Number of resize operations performed."""
        return self._resize_count
    
    def clear(self) -> None:
        """Clear all elements. Time Complexity: O(1)"""
        self._size = 0
    
    def to_list(self) -> List[Any]:
        """Convert to Python list. Time Complexity: O(n)"""
        return [self._data[i] for i in range(self._size)]


class Candle:
    """
    Represents a single OHLC candle with timestamp.
    """
    __slots__ = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    
    def __init__(self, timestamp: datetime, open_price: float, high: float, 
                 low: float, close: float, volume: float = 0.0):
        self.timestamp = timestamp
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
    
    def __repr__(self) -> str:
        return f"Candle({self.timestamp}, O={self.open:.2f}, H={self.high:.2f}, L={self.low:.2f}, C={self.close:.2f})"


class CandleStore:
    """
    Efficient storage and retrieval of OHLC candle data.
    
    Uses:
    - DynamicArray for storage (amortized O(1) insertion)
    - Manual Binary Search for timestamp lookups (O(log n))
    
    Assumes candles are inserted in chronological order.
    """
    
    def __init__(self):
        """Initialize empty candle store."""
        self._candles = DynamicArray()
        self._comparisons = 0  # Track comparisons for analysis
    
    def insert(self, candle: Candle) -> None:
        """
        Insert candle into store.
        Time Complexity: Amortized O(1)
        """
        self._candles.append(candle)
    
    def insert_from_dict(self, data: dict) -> None:
        """
        Insert candle from dictionary.
        Expected keys: timestamp, open, high, low, close, volume (optional)
        """
        candle = Candle(
            timestamp=data['timestamp'],
            open_price=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            volume=data.get('volume', 0.0)
        )
        self.insert(candle)
    
    def binary_search_timestamp(self, target_timestamp: datetime) -> int:
        """
        Manual binary search to find index of candle at or just before target timestamp.
        
        Time Complexity: O(log n)
        
        Returns:
            Index of candle, or -1 if not found / before all candles
        """
        self._comparisons = 0
        left = 0
        right = len(self._candles) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            self._comparisons += 1
            
            mid_ts = self._candles[mid].timestamp
            
            if mid_ts == target_timestamp:
                return mid
            elif mid_ts < target_timestamp:
                result = mid  # This could be the answer
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    def find_candle_at_timestamp(self, target_timestamp: datetime) -> Optional[Candle]:
        """
        Find exact candle at timestamp.
        Time Complexity: O(log n)
        """
        idx = self.binary_search_timestamp(target_timestamp)
        if idx >= 0 and self._candles[idx].timestamp == target_timestamp:
            return self._candles[idx]
        return None
    
    def get_range(self, start_ts: datetime, end_ts: datetime) -> List[Candle]:
        """
        Get all candles within time range [start_ts, end_ts].
        Time Complexity: O(log n + k) where k is number of candles in range
        """
        start_idx = self.binary_search_timestamp(start_ts)
        if start_idx < 0:
            start_idx = 0
        
        # Adjust if we landed before the start
        while start_idx < len(self._candles) and self._candles[start_idx].timestamp < start_ts:
            start_idx += 1
        
        result = []
        idx = start_idx
        while idx < len(self._candles) and self._candles[idx].timestamp <= end_ts:
            result.append(self._candles[idx])
            idx += 1
        
        return result
    
    def calculate_session_range(self, start_ts: datetime, end_ts: datetime) -> Tuple[float, float]:
        """
        Calculate high and low for a session time range.
        Time Complexity: O(log n + k) for k candles in session
        
        Returns:
            (session_high, session_low) tuple
        """
        candles = self.get_range(start_ts, end_ts)
        
        if not candles:
            return (0.0, 0.0)
        
        session_high = candles[0].high
        session_low = candles[0].low
        
        for candle in candles[1:]:
            if candle.high > session_high:
                session_high = candle.high
            if candle.low < session_low:
                session_low = candle.low
        
        return (session_high, session_low)
    
    def calculate_asia_range(self, date: datetime) -> Tuple[float, float]:
        """
        Calculate Asian session range (00:00 - 06:00 UTC) for a given date.
        Time Complexity: O(log n + k)
        """
        # Asian session: 00:00 - 06:00 UTC
        start_ts = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_ts = date.replace(hour=5, minute=55, second=0, microsecond=0)  # Last M5 candle in Asia
        
        return self.calculate_session_range(start_ts, end_ts)
    
    def __len__(self) -> int:
        """Return number of candles stored."""
        return len(self._candles)
    
    def __getitem__(self, index: int) -> Candle:
        """Access candle by index. Time Complexity: O(1)"""
        return self._candles[index]
    
    @property
    def last_comparisons(self) -> int:
        """Number of comparisons in last binary search."""
        return self._comparisons
    
    @property
    def resize_count(self) -> int:
        """Number of array resizes performed."""
        return self._candles.resize_count
    
    def get_stats(self) -> dict:
        """Get storage statistics."""
        return {
            'size': len(self._candles),
            'capacity': self._candles.capacity,
            'resize_count': self._candles.resize_count,
            'load_factor': len(self._candles) / self._candles.capacity if self._candles.capacity > 0 else 0
        }


# Demonstration functions
def demo_candle_store():
    """Demonstrate CandleStore functionality."""
    from datetime import timedelta
    
    print("=" * 60)
    print("Module 1: CandleStore (DynamicArray + Binary Search)")
    print("=" * 60)
    
    store = CandleStore()
    
    # Generate sample data
    base_time = datetime(2024, 1, 15, 0, 0, 0)
    print(f"\nInserting 1000 candles...")
    
    for i in range(1000):
        ts = base_time + timedelta(minutes=5 * i)
        candle = Candle(
            timestamp=ts,
            open_price=1900 + i * 0.1,
            high=1901 + i * 0.1,
            low=1899 + i * 0.1,
            close=1900.5 + i * 0.1,
            volume=1000 + i
        )
        store.insert(candle)
    
    stats = store.get_stats()
    print(f"✓ Inserted {stats['size']} candles")
    print(f"  - Array capacity: {stats['capacity']}")
    print(f"  - Resize operations: {stats['resize_count']}")
    print(f"  - Load factor: {stats['load_factor']:.2%}")
    
    # Binary search demo
    search_time = base_time + timedelta(hours=12)  # Search for noon candle
    print(f"\nBinary Search for {search_time}...")
    idx = store.binary_search_timestamp(search_time)
    
    if idx >= 0:
        found_candle = store[idx]
        print(f"✓ Found: {found_candle}")
        print(f"  - Comparisons made: {store.last_comparisons}")
        print(f"  - Expected O(log n) ≈ {int(3.32 * len(bin(len(store))) - 5)}")
    
    # Session range calculation
    print(f"\nCalculating Asian Session Range...")
    asia_high, asia_low = store.calculate_asia_range(base_time)
    print(f"✓ Asia High: {asia_high:.2f}")
    print(f"✓ Asia Low: {asia_low:.2f}")
    print(f"✓ Asia Range: {asia_high - asia_low:.2f}")
    
    return store


if __name__ == "__main__":
    demo_candle_store()

