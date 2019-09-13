"""
Package for working with raw JSON schema.
"""
from ._dynamic import string_schema, standard_object, constant, enum, number, regular_array, one_of, any_of
from ._error import JSONSchemaError
from ._static import TRIVIALLY_SUCCEED_SCHEMA, TRIVIALLY_FAIL_SCHEMA, BOOL_SCHEMA, INT_SCHEMA, FLOAT_SCHEMA, \
    STRING_SCHEMA, POSITIVE_INTEGER_SCHEMA, NEGATIVE_INTEGER_SCHEMA, NON_NEGATIVE_INTEGER_SCHEMA, \
    NON_POSITIVE_INTEGER_SCHEMA
from ._typing import JSONSchema, is_schema