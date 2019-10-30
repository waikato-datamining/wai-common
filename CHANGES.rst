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

0.0.4 (2019-09-13)
-------------------

- Two new iterable functions, all_meet_predicate and any_meets_predicate.
- Added meta-functions for determining if methods in base-classes have been overridden
  by sub-classes.
- Rejigged abc package.
- Added JSON package, with tools for working with JSON and JSONSchema. Also specifies the
  configuration class, which allows for easy manipulation of JSON files in an object-oriented
  manner.

0.0.5 (2019-09-17)
-------------------

- Added interfaces for serialising/deserialising JSON using custom representations.
- Added exception package to meta package for processing exceptions. Currently only
  contains ExceptionChainer, which captures exceptions as a context-manager and then
  provides methods for processing them.
- Added utility interface JSONValidatedBiserialisable.
- Refactored configurations and properties to be more understandable.
- Added AnyOfProperty.

0.0.6 (2019-09-17)
-------------------

- Fixed bug where Absent was being validated after Property.validate_value had checked
  it, and therefore failing.

0.0.7 (2019-09-18)
-------------------

- Added meta package for typing functionality.

0.0.8 (2019-09-19)
-------------------

- Fixed bug in get_argument_to_typevar.
- Added new property type for configurations, MapProperty, which behaves like a dict from
  strings to some sub-property type.
- Configurations now support: validation of additional properties, initialisation by value
  or JSON, programmatically getting/setting additional properties.

0.0.9 (2019-10-04)
-------------------

- Added StrictConfiguration, which disables additional properties by default.
- Minor fixes.

0.0.10 (2019-10-08)
-------------------

- JSON schema package now has tools for working with references/definitions.
- Configurations now validate additional properties as JSON by default.

0.0.11 (2019-10-09)
-------------------

- Fix so that JSON schema definitions propagate through all composite schema.

0.0.12 (2019-10-09)
-------------------

- Added support for checking Python versions.
- get_argument_to_typevar now works with Python3.6 and Python3.7.

0.0.13 (2019-10-09)
-------------------

- Fixed bug in Configuration where cached schema were preventing grand-inheritance.

0.0.14 (2019-10-09)
-------------------

- Configuration schema caching is now lazier than ever.
- JSON serialisation now validates in both directions.

0.0.15 (2019-10-09)
-------------------

- Bug fixes.

0.0.16 (2019-10-22)
-------------------

- Added support for ADAMS report files.
- Added basic support for geometry.
- Added support for working with located objects in image-classification/identification
  tasks.

0.0.17 (2019-10-31)
-------------------

- Added TypeVarProperty, for easier caching of dynamic type variables.
- Added depth argument to flatten (iterators and sequences).
