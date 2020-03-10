from typing import Any, Optional

from ...meta import non_default_kwargs
from ..._ClassRegistry import ClassRegistry
from .._typing import OptionsList
from ._Option import Option


class ClassRegistryOption(Option):
    """
    Option which selects a class from a class registry.
    Selection can only be made from aliases.
    """
    def __init__(self,
                 *flags: str,
                 registry: ClassRegistry,
                 required: bool = ...,
                 metavar: str = ...,
                 help: str = ...):
        # Save the registry
        self._registry: ClassRegistry = registry

        super().__init__(*flags,
                         choices=registry.aliases(),
                         **non_default_kwargs(ClassRegistryOption.__init__, locals()))

    def _namespace_value_to_internal_value(self, namespace_value: Optional[str]) -> Optional[type]:
        if namespace_value is None:
            return None
        return self._registry.find(namespace_value)

    def _internal_value_to_namespace_value(self, internal_value: Optional[type]) -> Optional[str]:
        return self._registry.get_alias(internal_value)

    def _namespace_value_to_options_list(self, namespace_value: Optional[str]) -> OptionsList:
        pass

    def _validate_internal_value(self, internal_value: Any):
        # Internal values are classes
        if not isinstance(internal_value, type):
            raise TypeError(f"Class-registry option expects classes for internal values")

        # Make sure it's an aliased class
        if self._registry.get_alias(internal_value) is None:
            raise ValueError(f"Type '{internal_value.__qualname__}' is not a valid type for this option")

    def _validate_namespace_value(self, namespace_value: Any):
        # Namespace value should be a string
        if not isinstance(namespace_value, str):
            raise TypeError(f"Class-registry options expect string namespace values")

        if not self._registry.has_alias(namespace_value):
            raise NameError(f"Registry has no alias '{namespace_value}'")
