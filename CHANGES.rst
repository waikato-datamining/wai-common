Changelog
=========

0.0.1 (2019-08-09)
-------------------

- Initial release

0.0.2 (2019-08-09)
-------------------

- Removed restriction that switch only work with enums. Now can switch on any type.
  Onus is on the user to handle modifications of the switched value during switching.
- Added **abc** package, with utilities for working with abstract classes/methods.
- Added **decorator** package, with custom decorators.

0.0.3 (2019-08-30)
-------------------

- Added load_dir function to file package, which can load all files in a directory.
- Added is_hashable to test if an object is hashable.
- Added Interval class representing intervals on the number line.
- Added exception InvalidStateError for classes that get into an invalid setup.
- Added typing module for type-related functionality.
- Added first, which finds the first element of an iterable to match a predicate.
- Added statistics package with quartile functions.
- Added random, which returns the elements of an iterator in random order.
- Added meta package, with functions to set and retrieve arbitrary meta-data against
  objects.
- Added ConstantIterator class, which returns the same value over and over again.
- Added metadata module to iterate, for working with metadata in iterables of objects.
- Modified TwoWayDict so type-inference works with Python-3.7.
