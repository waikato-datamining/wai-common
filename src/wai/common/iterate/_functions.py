from typing import Iterable, Iterator, Optional


def safe_iter(obj) -> Optional[Iterator]:
    """
    Returns an iterator for the object if it's iterable,
    or None if it's not.

    :param obj:     The object to get the iterator for.
    :return:        The iterator, or None if it's not iterable.
    """
    try:
        return iter(obj)
    except Exception:
        return None


def flatten(iterable: Iterable) -> Iterator:
    """
    Gets an iterator for the given iterable, which will
    flatten any iterable elements into the iterator output.

    :param iterable:    The iterable.
    :return:            A flattening iterator over the iterable.
    """
    # Process each element of the iterable in turn
    for element in iterable:
        # Try to get an iterator for the element
        element_iter = safe_iter(element)

        # If the element isn't iterable, yield the element itself
        if element_iter is None:
            yield element

        # Otherwise yield each sub-element of the flattened element
        for sub_element in flatten(element_iter):
            yield sub_element


def invert_indices(indices: Iterable[int], size: int) -> Iterator[int]:
    """
    Returns the indices that are not in the given indices, up to the given size.

    :param indices:     The indices to invert.
    :param size:        The exclusive maximum index.
    :return:            A inverted indices.
    """
    index_set = set(indices)

    for i in range(size):
        if i not in index_set:
            yield i
