from typing import List, Optional


class CSVFile:
    """
    Class representing a CSV file loaded into memory.
    """
    def __init__(self,
                 header: Optional[List[str]] = None,
                 data: List[List[any]] = None):
        self.header = header
        if data is None:
            data = []
        self.data = data

    def get_column(self, column_index):
        """
        Gets a column of data.

        :param column_index:    The column to copy.
        :return:                The column of data (as a list).
        """
        return [row[column_index] for row in self.data]
