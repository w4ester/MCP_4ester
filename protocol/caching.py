class SimpleCache:
    """Simple in-memory cache implementation.
    In production, consider using Redis or another distributed cache.
    """
    
    def __init__(self):
        """Initialize an empty cache store."""
        self.store = {}
    
    def get(self, key: str) -> str:
        """Get a value from the cache.
        
        Args:
            key (str): Cache key
            
        Returns:
            str: Cached value or None if not found
        """
        return self.store.get(key)
    
    def set(self, key: str, value: str) -> None:
        """Set a value in the cache.
        
        Args:
            key (str): Cache key
            value (str): Value to cache
        """
        self.store[key] = value
    
    def clear(self) -> None:
        """Clear all cached values."""
        self.store.clear()