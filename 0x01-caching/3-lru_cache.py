#!/usr/bin/python3
"""
LRU cache
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """class for implementing LRU"""
    def __init__(self):
        """construct class"""
        super().__init__()
        self.least_used = []

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.least_used.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # If cache is full, discard the least recently used item
            lru_key = self.least_used.pop(0)
            print("DISCARD:", lru_key)
            del self.cache_data[lru_key]

        # Update the order and cache data
        self.least_used.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """get values based on key"""
        value = self.cache_data[key] if key and key \
            in self.cache_data.keys() else None
        return value
