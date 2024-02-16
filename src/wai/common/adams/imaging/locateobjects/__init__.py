"""
Package for working with located objects in image classification/identification tasks.
"""
from ._LocatedObject import LocatedObject
from ._LocatedObjects import LocatedObjects
from ._NormalizedLocatedObject import NormalizedLocatedObject
from ._NormalizedLocatedObjects import NormalizedLocatedObjects
from ._convert import absolute_to_normalized, normalized_to_absolute
