"""
Provides memoisation of function calls.

For long-running functions, it is sometimes nice to store the result,
and then simply load it the next time the function is called with the same
parameters. This module uses pickle to store the result to disk, and to
load it again.

Instead of:

    result = func(*args, **kwargs)

you would call:

    result = memoise(func, *args, **kwargs, path="/path/to/memo/files/")

The first call will run the function as usual, but subsequent calls will load
the result from disk instead.

N.B.:
    - All arguments to the function and the function's result must be picklable.
    - Function state/closures are not pickled. Should only be used with pure functions.
"""
import hashlib
import os
import pickle
from typing import Callable, Tuple, Dict, Any


def memoise(func: Callable, *args, path: str = "." + os.sep, **kwargs):
    """
    Memoises the result of a function with Pickle, so that long-running
    functions can be sped up at the expense of disk space. Should only be
    used with pure functions, as internal state is not taken into account.

    :param path:        The name of the directory to store the pickle file in.
    :param func:        The function to call.
    :param args:        The positional arguments to the function.
    :param kwargs:      The keyword arguments to the function.
    :return:            The result of calling the function.
    """
    # Make sure the directory ends with a separator
    if not path.endswith(os.sep):
        path += os.sep

    # Create the directory if it doesn't exist
    if not os.path.exists(path):
        os.mkdir(path)

    # Turn the kwargs dict into a tuple
    picklable_kwargs: PicklableDict = PicklableDict(kwargs)

    # Pickle the function and its argument and create a hash
    # from the bytes
    pickled_func_and_args = pickle.dumps((func, args, picklable_kwargs))
    arg_hash = hashlib.sha256(pickled_func_and_args).hexdigest()

    # Hash the function code so we can invalidate when it changes
    code_hash = hashlib.sha256(func.__code__.co_code).digest()

    # Create a filename from the hash
    filename: str = path + arg_hash[-16:] + ".memo"

    # Attempt to read the results from file
    try:
        with open(filename, "rb") as file:
            stored_func_and_args = file.read(len(pickled_func_and_args))
            stored_code_hash = file.read(len(code_hash))

            if pickled_func_and_args == stored_func_and_args and code_hash == stored_code_hash:
                return pickle.load(file)
    except Exception:
        pass

    # Generate the result
    result = func(*args, **kwargs)

    # Memoise the result for next time
    with open(filename, "wb") as file:
        file.write(pickled_func_and_args)
        file.write(code_hash)
        pickle.dump(result, file)

    return result


class PicklableDict:
    """
    Class which is a picklable representation of a dictionary
    (assuming all keys/values are picklable).
    """
    def __init__(self, dictionary: Dict[Any, Any]):
        # The internal representation of the dictionary
        self.intern: Tuple[Tuple[Any, Any], ...] = tuple(dictionary.items())

    def __eq__(self, other):
        if isinstance(other, PicklableDict):
            other = other.to_dict()

        if isinstance(other, dict):
            return other == self.to_dict()

        return False

    def to_dict(self) -> Dict[Any, Any]:
        """
        Reconstructs the dictionary.

        :return:    The dictionary.
        """
        return {key: value for key, value in self.intern}
