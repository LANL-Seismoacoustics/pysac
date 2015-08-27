# Manual

## pysac.header

SAC header specification, including documentation.

Header names, order, and types, nulls, as well as allowed enumerated values, are
specified here.  Header name strings, and their array order are contained in
separate float, int, and string tuples.  Enumerated values, and their allowed
string and integer values, are in dictionaries.  Header value documentation is
in a dictionary, for reuse throughout the package.


## pysac.util

SAC module helper functions and data.


## pysac.arrayio

Low-level array interface to the SAC file format.

Functions in this module work directly with numpy arrays that mirror the SAC
format.  The 'primitives' in this module are the float, int, and string header
arrays, the float data array, and a header dictionary. Convenience functions
are provided to convert between header arrays and more user-friendly
dictionaries.

These read/write routines are very literal; there is almost no value or type
checking, except for byteorder and header/data array length.  File- and array-
based checking routines are provided for additional checks where desired.


## pysac.sactrace

Object-oriented interface to the SAC file format.

The SACTrace object maintains consistency between SAC headers and manages
header values in a user-friendly way. This includes some value-checking, native
Python logicals (True, False) and nulls (None) instead of SAC's 0, 1, or -12345...

SAC headers are implemented as properties, with appropriate getters and setters.

