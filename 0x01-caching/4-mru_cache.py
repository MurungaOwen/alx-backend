#!/usr/bin/python3
"""
MRU caching
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """class for implementing MRU"""
    def __init__(self):
        """ Initialize the MRUCache """
        super().__init__()
        self.access_order = []  # order based on MRU

    def put(self, key, item):
        """ Add an item to the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # If key already exists, remove it
            self.access_order.remove(key)
        elif len(self.cache_data) >= self.MAX_ITEMS:
            # If cache is full, discard the most recently used item
            mru_key = self.access_order.pop()
            print("DISCARD:", mru_key)
            del self.cache_data[mru_key]

        # Update the access order and cache data with the new item
        self.access_order.append(key)
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item from the cache """
        if key is None:
            return None

        if key in self.cache_data:
            # If key exists, update the access order and return the item
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache_data[key]
        else:
            return None
