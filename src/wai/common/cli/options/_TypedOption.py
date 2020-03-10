from argparse import REMAINDER
from typing import Union, Any, Type, Iterable, Tuple, TypeVar, List

from ...meta import non_default_kwargs
from .._CLIRepresentable import CLIRepresentable, cli_repr, from_cli_repr
from .._typing import OptionsList
from ._Option import Option

# The type of class the option takes
ClassType = TypeVar("ClassType", bound=CLIRepresentable)

# The set of actions allowed with this type of option
ALLOWED_ACTIONS = {"store", "append"}


class TypedOption(Option):
    """
    An option which takes a specified type of CLI-representable objects as values.
    """
    def __init__(self,
                 *flags: str,
                 type: Type[ClassType],
                 action: str = ...,
                 nargs: Union[int, str] = ...,
                 choices: Iterable[Union[str, ClassType]] = ...,
                 default: Union[ClassType, List[ClassType], None] = ...,
                 required: bool = ...,
                 help: str = ...,
                 metavar: Union[str, Tuple[str, ...]] = ...):
        # Check the type is CLI-representable
        if not CLIRepresentable.type_check(type):
            raise TypeError(f"Type {type.__qualname__} is not a CLI-representable type")
        self._type = type

        # Check the action is allowed
        if action is not ... and action not in ALLOWED_ACTIONS:
            raise ValueError(f"Action must be one of {ALLOWED_ACTIONS}")
        self._action = action if action is not ... else "store"

        # Check the number of arguments is allowed
        if nargs == "?" or nargs == REMAINDER:
            raise ValueError(f"Disallowed nargs value {nargs}")
        self._nargs = nargs if nargs is not ... else None

        # Save our optional status
        self._optional = not required if required is not ... else True

        # See if our values should be list-valued or not
        self._is_list_valued = action == "append" or nargs is not ...

        # Format choices as strings
        if choices is not ...:
            formatted_choices = []
            for choice in choices:
                # Convert CLI representations into actual objects
                if isinstance(choice, str):
                    choice = from_cli_repr(type, choice)

                # Make sure they are instances of the defined type
                if not isinstance(choice, type):
                    raise TypeError(f"Choice is not of the declared type")

                formatted_choices.append(cli_repr(choice))
            choices = formatted_choices

        # Format default value
        if default is not ...:
            formatted_default = self._internal_value_to_namespace_value(default)
        else:
            formatted_default = [] if self._is_list_valued else None

        # Extract the set of keyword arguments
        kwargs = non_default_kwargs(TypedOption.__init__, locals())

        super().__init__(*flags, default=formatted_default, **kwargs)

        self._update_kwargs_repr("type", type, True)
        for name, value in kwargs.items():
            self._update_kwargs_repr(name, value, True)

    @property
    def type(self) -> Type[ClassType]:
        """
        Gets the type of value this option takes.
        """
        return self._type

    def _namespace_value_to_internal_value(self, namespace_value: Any) -> Any:
        if isinstance(namespace_value, list):
            return [from_cli_repr(self._type, cli_string) for cli_string in namespace_value]
        elif isinstance(namespace_value, str):
            return from_cli_repr(self._type, namespace_value)
        else:
            return None

    def _internal_value_to_namespace_value(self, internal_value: Any) -> Any:
        if isinstance(internal_value, list):
            return [cli_repr(cli_string) for cli_string in internal_value]
        elif isinstance(internal_value, str):
            return cli_repr(internal_value)
        else:
            return None

    def _namespace_value_to_options_list(self, namespace_value: Any) -> OptionsList:
        if isinstance(namespace_value, list):
            length = len(namespace_value)
            nargs = self._nargs if self._nargs is not None else 1
            options_list = []
            if self._optional and length == 0:
                pass
            if self._action == "store" or isinstance(nargs, str):
                options_list.append(self._flags[0])
                for val in namespace_value:
                    options_list.append(cli_repr(val))
            else:
                for i in range(0, len(namespace_value), nargs):
                    options_list.append(self._flags[0])
                    for val in namespace_value[i:i + nargs]:
                        options_list.append(cli_repr(val))
            return options_list
        else:
            if self._optional and namespace_value is None:
                return []
            return [self._flags[0], namespace_value]

    def _validate_namespace_value(self, namespace_value: Any):
        if self._is_list_valued:
            if not isinstance(namespace_value, list):
                raise TypeError(f"Class option expects namespace values as lists")

            if not all(isinstance(element, str) for element in namespace_value):
                raise TypeError(f"Class option expects all elements of namespace list to be strings")
        elif not self._optional or namespace_value is not None:
            if not isinstance(namespace_value, str):
                raise TypeError(f"Class option expects namespace values as strings")

    def _validate_internal_value(self, internal_value: Any):
        if self._is_list_valued:
            self._validate_internal_value_list(internal_value)
        else:
            self._validate_internal_value_singular(internal_value)

    def _validate_internal_value_singular(self, value: Any):
        """
        Validate's the given value when trying to set the value
        of this option. Assumes the value should be a singular value.

        :param value:       The value attempting to be set.
        :return:            The actual value that should be set.
        :raises Exception:  If the value cannot be validated.
        """
        # Make sure the value is of our type (or None if we're optional)
        if not self._optional or value is not None:
            if not isinstance(value, self._type):
                raise TypeError(f"Expected {self._type.__name__} but got {type(value).__name__}")

    def _validate_internal_value_list(self, value: Any):
        """
        Validate's the given value when trying to set the value
        of this option. Assumes the value should be a list of values.

        :param value:       The value attempting to be set.
        :return:            The actual value that should be set.
        :raises Exception:  If the value cannot be validated.
        """
        # Make sure the value is a list
        if not isinstance(value, list):
            raise TypeError(f"Value must be a list")

        # Make sure the list has the correct number of values in it
        length = len(value)
        if self._optional and length == 0:
            pass
        elif isinstance(self._nargs, int):
            if self._action == "store":
                if length != self._nargs:
                    raise ValueError(f"Requires list of length {self._nargs}")
            else:
                if length % self._nargs != 0:
                    raise ValueError(f"Requires list of length a multiple of {self._nargs}")
        elif self._nargs == "+":
            if length == 0:
                raise ValueError(f"Requires at least one item")

        if any(not isinstance(element, self._type) for element in value):
            raise TypeError(f"All values must be of the declared type {self._type.__name__}")