#!/usr/bin/env python3
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """find start and end of tuple"""
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """gets data based on page num
        params:
            page, page_size
        return:
            a list of data based on page no.
        """
        assert isinstance(page, int) and page > 0, \
            "page must be positive"
        assert isinstance(page_size, int) and page_size > 0, \
            "page_Size must be positive"
        data = self.dataset()
        index_value_range = index_range(page, page_size)
        start, end = index_value_range
        filtered_data = data[start: end]
        return [] if not filtered_data else filtered_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """to get the hper link"""
        data = self.get_page(page, page_size)
        total_data = len(self.dataset())
        total_pages = total_data / page_size
        next_page = page + 1 if page <= total_pages else None
        prev_page = page - 1 if page - 1 > 0 else None
        hyper = {
            'page_size': page_size,
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': int(total_pages)
        }
        return hyper
