import logging


def create_standard_library_root_logger(library_root_package: str) -> logging.Logger:
    """
    Creates a root logger for libraries. This is a logger
    with a single null handler attached to it so that libraries
    can be used without logging set up.

    :param library_root_package:    The package name of the library.
    :return:                        The created logger.
    """
    # Get the logger for the package
    library_root_logger: logging.Logger = logging.getLogger(library_root_package)

    # Add a null-handler to it if it doesn't have any already
    if len(library_root_logger.handlers) == 0:
        library_root_logger.addHandler(logging.NullHandler())

    return library_root_logger
