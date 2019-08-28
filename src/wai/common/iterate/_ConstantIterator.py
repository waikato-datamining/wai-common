from collections import Iterator
from typing import _T_co, Optional


class ConstantIterator(Iterator[_T_co]):
    """
    Class which implements the iterator interface, but always returns a single value.
    """
    def __init__(self, value: _T_co, num_iterations: Optional[int] = None):
        self._value: _T_co = value
        self._num_iterations: Optional[int] = num_iterations

    def __next__(self) -> _T_co:
        if self._num_iterations == 0:
            raise StopIteration
        elif self._num_iterations is not None:
            self._num_iterations -= 1

        return self._value
