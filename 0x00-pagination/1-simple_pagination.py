#!/usr/bin/env python3
import csv
import math
from typing import List

ind_range = __import__('0-simple_helper_function').index_range


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
        assert isinstance(page, int) and page > 0, \
            "page must be positive"
        assert isinstance(page_size, int) and page_size > 0, \
            "page_Size must be positive"
        index_value_range = ind_range(page, page_size)
        data = self.dataset()
        values = []