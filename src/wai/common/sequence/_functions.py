from typing import Sequence, Any, Iterable, Iterator, Union


def normalise_index(index: int, length: Union[int, Sequence]) -> int:
    """
    Normalises the given list index into the valid range for a
    list of the given length. This way negative indices index
    backward from the end of the list.

    :param index:   The index to normalise.
    :param length:  The sequence length to normalise to, or a sequence.
    :return:        The normalised index.
    """
    # Get the length if we're given a sequence
    if not isinstance(length, int):
        length = len(length)

    return index % length


def extract_by_index(sequence: Sequence[Any], indices: Iterable[int]) -> Iterator[Any]:
    """
    Extracts elements of the given sequence.

    :param sequence:    The sequence to get elements from.
    :param indices:     The indices of the elements to get.
    :return:            The selected elements.
    """
    for index in indices:
        yield sequence[index]


def binary_search(sequence: Sequence[int], target: int) -> int:
    """
    Performs as binary search on an ordered sequence of ints to
    find the index of the first value greater than or equal to
    the target value.

    :param sequence:    The order sequence of ints.
    :param target:      The target value to find.
    :return:            The index of the found element.
    """
    start = 0
    end = len(sequence)
    while end != start:
        pivot = (start + end) // 2
        if sequence[pivot] >= target:
            end = pivot
        else:
            start = pivot + 1

    return start
