from inspect import signature, Signature, Parameter
from typing import Any, Dict, Tuple, Callable

from ._import_code import get_import_code

# The types of a code-representation
ImportDict = Dict[str, str]
CodeRepresentation = Tuple[ImportDict, str]

# The type of the code_repr function
CodeReprFunction = Callable[[Any], CodeRepresentation]


def type_code_repr(cls) -> CodeRepresentation:
    """
    The code_repr function for types.

    :param cls:     The type to get the code representation for.
    :return:        The code representation of the type.
    """
    # Get the import code for the class
    import_code = get_import_code(cls, alias_inner_class=False)

    return {cls.__qualname__: import_code}, cls.__qualname__


# The honorary code-representable types, and their code_repr methods.
HONORARY_MEMBERS: Dict[type, CodeReprFunction] = {
    type: type_code_repr,
    str: lambda string: ({}, repr(string)),
    int: lambda integer: ({}, repr(integer)),
    bool: lambda boolean: ({}, repr(boolean)),
    None: lambda none: ({}, repr(none))
}


class CodeRepresentable:
    """
    Base class for types that can represent themselves as a Python expression which,
    when evaluated, evaluates to a copy of themselves.
    """
    def code_repr(self) -> CodeRepresentation:
        """
        Gets the code representation of the object.

        :return:    The code representation.
        """
        raise NotImplementedError(CodeRepresentable.code_repr.__qualname__)

    @staticmethod
    def isinstance(obj) -> bool:
        """
        Checks if the given object is code-representable.

        :param obj:     The object to check.
        :return:        True if the object is code-representable,
                        False if not.
        """
        return type(obj) in HONORARY_MEMBERS or isinstance(obj, CodeRepresentable)

    @staticmethod
    def issubclass(cls) -> bool:
        """
        Checks if the given class is a code-representable type.

        :param cls:     The class to check.
        :return:        True if the class is a code-representable type,
                        False if not.
        """
        return cls in HONORARY_MEMBERS or issubclass(cls, CodeRepresentable)


def code_repr(obj: Any) -> CodeRepresentation:
    """
    Gets the code representation of the object.

    :return:    The code representation.
    """
    # Make sure the object is code-representable
    if not CodeRepresentable.isinstance(obj):
        raise TypeError(f"Object '{obj}' is not code-representable")

    if type(obj) in HONORARY_MEMBERS:
        return HONORARY_MEMBERS[type(obj)](obj)

    return obj.code_repr()


# ========= #
# UTILITIES #
# ========= #


def get_import_dict(code_representation: CodeRepresentation) -> ImportDict:
    """
    Gets the import dictionary from a code representation.

    :param code_representation:     The code representation.
    :return:                        The import dictionary.
    """
    return code_representation[0]


def get_code(code_representation: CodeRepresentation) -> str:
    """
    Gets the code from a code representation.

    :param code_representation:     The code representation.
    :return:                        The code.
    """
    return code_representation[1]


def combine_import_dicts(*import_dicts: ImportDict) -> ImportDict:
    """
    Combines multiple import dictionaries into one, ensuring no
    imported names are lost.

    :param import_dicts:    The import dictionaries to combine.
    :return:                The combined import dictionary.
    """
    result = {}

    for import_dict in import_dicts:
        for imported_name, import_code in import_dict.items():
            if imported_name in result:
                if import_code != result[imported_name]:
                    raise ValueError(f"Multiple conflicting imports with name '{imported_name}'\n"
                                     f"{import_code}\n"
                                     f"<->\n"
                                     f"{result[imported_name]}")
            else:
                result[imported_name] = import_code

    return result


def from_init(self, locals_) -> CodeRepresentation:
    """
    Utility for when the code-representation is completely
    determined in the __init__ method by the arguments passed
    to that method.

    :param self:        The object being initialised.
    :param locals_:     The local scope of the __init__ method.
    :return:            The code-representation for the object.
    """
    # Get the type being initialised
    cls = type(self)

    # Initialise the import dict with the import for the class itself
    import_dict = get_import_dict(code_repr(cls))

    # Get the method signature of the __init__ method
    init_signature: Signature = signature(self.__init__)

    # Start the representation
    code = f"{cls.__qualname__}("

    # Format each argument in turn
    first = True
    for name, parameter in init_signature.parameters.items():
        parameter_string = ""
        value = locals_[name]
        if parameter.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY}:
            if value is not parameter.default:
                value_repr = code_repr(value)
                import_dict = combine_import_dicts(import_dict, get_import_dict(value_repr))
                parameter_string = (f"{name}={get_code(value_repr)}"
                                    if parameter.kind == Parameter.KEYWORD_ONLY
                                    else get_code(value_repr))
        elif parameter.kind == Parameter.VAR_POSITIONAL:
            if len(value) > 0:
                value_reprs = tuple(map(code_repr, value))
                import_dict = combine_import_dicts(import_dict, *map(get_import_dict, value_reprs))
                parameter_string = ", ".join(map(get_code, value_reprs))
        elif parameter.kind == Parameter.VAR_KEYWORD:
            if len(value) > 0:
                value_reprs = {key: code_repr(value) for key, value in value.items()}
                import_dict = combine_import_dicts(import_dict, *map(get_import_dict, value_reprs.values()))
                parameter_string = ", ".join(f"{key}={get_code(value_repr)}" for key, value_repr in value_reprs.items())

        if parameter_string != "":
            if not first:
                code += ", "
            else:
                first = False
            code += parameter_string

    code += ")"

    return import_dict, code
