#!/usr/bin/env python3
"""define index_range"""


def index_range(page: int, page_size: int) -> tuple:
    """find start and end of tuple"""
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)
