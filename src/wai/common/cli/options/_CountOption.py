from typing import Optional, Any

from ..constants import SHORT_FLAG_PREFIX
from ..util import is_short_flag, \
    TranslationDict, TranslationDictPair, create_translation_pair, translate_forward, translate_reverse
from .._typing import OptionsList
from ._Option import Option


class CountOption(Option):
    """
    Option which counts the number of times its flag appears.

    Can optionally supply a translation table to translate from
    actual count values to some other set of integers (e.g. from
    counts to verbosity values).
    """
    def __init__(self,
                 *flags: str,
                 translation: Optional[TranslationDict] = None,
                 help: str = ...):
        super().__init__(*flags,
                         action="count",
                         default=0,
                         help=help)

        self._update_kwargs_repr("translation", translation, translation is not None)
        self._update_kwargs_repr("help", help, help is not ...)

        self._translations: Optional[TranslationDictPair] = create_translation_pair(translation)

    def _namespace_value_to_internal_value(self, namespace_value: Any) -> int:
        return translate_forward(namespace_value, self._translations)

    def _internal_value_to_namespace_value(self, value: Any) -> int:
        return translate_reverse(value, self._translations)

    def _namespace_value_to_options_list(self, namespace_value: Any) -> OptionsList:
        # If count is 0, return no options
        if namespace_value == 0:
            return []

        # Try to use a short flag if available, otherwise just the first flag
        selected_flag = self.flags[0]
        short_flag = is_short_flag(selected_flag)
        if len(self.flags) == 2 and not short_flag:
            selected_flag = self.flags[1]
            short_flag = True

        # Iterate the flag count times
        if short_flag:
            return [SHORT_FLAG_PREFIX + selected_flag[1] * namespace_value]
        else:
            return [selected_flag] * namespace_value

    def _validate_internal_value(self, internal_value: Any):
        # Value must be an integer
        if not isinstance(internal_value, int):
            raise TypeError(f"Count options take integer values, not {internal_value}")

    def _validate_namespace_value(self, namespace_value: Any):
        if not isinstance(namespace_value, int):
            raise TypeError(f"Count options expect integer namespace values, not {namespace_value}")