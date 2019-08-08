import gzip


def get_open_func(filename):
    """
    Gets the open function to use to open the given filename.

    :param filename:    The file to open.
    :return:            The open function, and the read-mode flag to use.
    """

    # Select the open function based on the filename
    if filename.endswith('.gz'):
        return gzip.open, 'rt'
    else:
        return open, 'r'
