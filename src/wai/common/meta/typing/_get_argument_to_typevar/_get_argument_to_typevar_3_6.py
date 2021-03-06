from typing import Type, TypeVar

import typing_inspect

from ._get_argument_to_typevar_base import check_args


def get_argument_to_typevar(cls: Type, generic_base_class: Type, typevar: TypeVar):
    """
    Gets the argument given to a type variable parameterising
    a generic base class in a particular sub-class of that base.

    :param cls:                 The sub-class specifying the argument.
    :param generic_base_class:  The generic base-class specifying the type variable.
    :param typevar:             The type variable to get the argument for.
    :return:                    The argument to the type variable.
    """
    # Check the arguments
    typevar_index: int = check_args(cls, generic_base_class, typevar)

    # Get the decendency path from derived to base class
    bases = [cls]
    while bases[-1] is not generic_base_class:
        # Keep track of if we found a base
        base_found = False

        # Try and find a generic base
        for base in typing_inspect.get_generic_bases(bases[-1]):
            if issubclass(base, generic_base_class):
                bases.append(base)
                base_found = True
                break

        # If we didn't find a generic base, find a non-generic base
        if not base_found:
            for base in bases[-1].__bases__:
                if issubclass(base, generic_base_class):
                    bases.append(base)
                    break

    # Search the dependency path for the type variable's final argument
    arg = None
    while len(bases) > 1:
        # Get the arguments to the generic base class
        args = typing_inspect.get_args(bases[-2])

        # If no arguments are given, the signature stays the same
        if len(args) == 0:
            bases = bases[:-2] + bases[-1:]
            continue

        # Get the argument to this typevar
        arg = args[typevar_index]

        # If it's another type variable, keep looking for the argument to this
        # type variable
        if typing_inspect.is_typevar(arg):
            typevar_index = typing_inspect.get_parameters(bases[-2]).index(arg)
            bases = bases[:-1]
            continue

        # Otherwise return the argument to the type variable
        return arg

    return arg
