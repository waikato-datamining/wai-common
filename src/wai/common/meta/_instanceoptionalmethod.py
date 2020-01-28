from functools import wraps


class instanceoptionalmethod:
    """
    Decorator class (like classmethod/staticmethod) which provides
    the class as the first implicit parameter, and the instance as
    the second (if called on an instance) or None (if not).
    """
    def __init__(self, function):
        self._function = function

    def __get__(self, instance, owner):
        @wraps(self._function)
        def intern(*args, **kwargs):
            return self._function(owner, instance, *args, **kwargs)

        return intern
