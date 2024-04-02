#!/usr/bin/python3
""" BasicCaching module
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """class for implementing Basic cache"""
    def __init__(self):
        """constructor"""
        super().__init__()

    def put(self, key, item):
        """insert items in cache"""
        self.cache_data[key] = item \
            if key and item else None

    def get(self, key):
        """get values based on keys"""
        value = self.cache_data[key] \
            if key in self.cache_data.keys() else None
        return value
