#!/usr/bin/python3
"""
FIFO caching
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """class for implementing FIFO"""
    def __init__(self):
        """initialise class"""
        super().__init__()

    def put(self, key, item):
        """
        insert data into cache
        """
        my_dict = self.cache_data
        if key and item:
            if len(my_dict) < self.MAX_ITEMS:
                my_dict[key] = item
            else:
                pop_key = next(iter(my_dict))
                print(f"DISCARD: {pop_key}")
                del my_dict[pop_key]
            my_dict[key] = item
        else:
            return None

    def get(self, key):
        """get values based on key"""
        value = self.cache_data[key] if key and key \
            in self.cache_data.keys() else None
        return value
