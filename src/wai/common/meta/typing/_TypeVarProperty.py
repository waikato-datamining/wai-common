from typing import TypeVar

from ._get_argument_to_typevar import get_argument_to_typevar


class TypeVarProperty:
    """
    Property class which caches the dynamic type of a type-variable
    for a class.
    """
    def __init__(self, typevar: TypeVar):
        self._typevar: TypeVar = typevar
        self._base_class = None
        self._cache = None

    def __get__(self, instance, owner):
        if self._cache is None:
            self._cache = get_argument_to_typevar(type(instance), self._base_class, self._typevar)
            del self._typevar
            del self._base_class

        return self._cache

    def __set_name__(self, owner, name):
        # Prevents reassignment to parameterised generic base class
        if self._base_class is not None:
            return

        self._base_class = owner