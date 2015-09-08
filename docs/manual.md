# Package Organization

## pysac.header

SAC header specification, including documentation.

Header names, order, and types, nulls, as well as allowed enumerated values, are
specified here.  Header name strings, and their array order are contained in
separate float, int, and string tuples.  Enumerated values, and their allowed
string and integer values, are in dictionaries.  Header value documentation is
in a dictionary, `DOC`, for reuse throughout the package.


## pysac.util

PySAC helper functions and data.  Contains functions to validate and convert
enumerated values, byteorder consistency checking, and SAC reference time
reading.

Two of the most important functions in this module are `sac_to_obspy_header`
and `obspy_to_sac_header`.  These contain the conversion routines between SAC
header dictionaries and ObsPy header dictionaries.  **These functions control
the way ObsPy reads and writes SAC files,** which was one of the main
motivations for authoring this package.


## pysac.arrayio

Low-level array interface to the SAC file format.

Functions in this module work directly with numpy arrays that mirror the SAC
format, and comprise much of the machinery that underlies the `SACTrace` class.
The 'primitives' in this module are the float, int, and string header arrays,
the float data array, and a header dictionary. Convenience functions are
provided to convert between header arrays and more user-friendly dictionaries.

These read/write routines are very literal; there is almost no value or type
checking, except for byteorder and header/data array length.  File- and array-
based checking routines are provided for additional checks where desired.

Reading and writing are done with `read_sac` and `write_sac` for binary SAC
files, and `read_sac_ascii` and `write_sac_ascii` for alphanumeric files.
Conversions between header dictionaries and the three SAC header arrays are done
with the `header_arrays_to_dict` and `dict_to_header_arrays` functions.
Validation of header values and data is managed by `validate_sac_content`,
which can currently do six different tests.


## pysac.sactrace

Contains the `SACTrace` class, which is the main user-facing interface to the
SAC file format.

The `SACTrace` object maintains consistency between SAC headers and manages
header values in a user-friendly way. This includes some value-checking, native
Python logicals and nulls instead of SAC's header-dependent logical/null
representation.


### Reading and writing SAC files

PySAC can read and write evenly-spaced time-series files.  It supports big or
little-endian binary files, or alphanumeric/ASCII files.

```python
# read from a binary file
sac = SACTrace.read(filename)

# read header only
sac = SACTrace.read(filename, headonly=True)

# write header-only, file must exist
sac.write(filename, headonly=True)

# read from an ASCII file
sac = SACTrace.read(filename, ascii=True)

# write a binary SAC file for a Sun machine
sac.write(filename, byteorder='big')
```

### Headers

In the `SACTrace` class, SAC headers are implemented as properties, with
appropriate *getters* and *setters*.  The getters/setters translate user-facing
native Python values like `True`, `False`, and `None` to the appropriate SAC
header values, like `1`, `0`, `-12345`, `'-12345   '`, etc.  

Header values that depend on the SAC `.data` vector are calculated on-the-fly,
and fall back to the stored header value.

A convenient read-only dictionary of non-null, raw SAC header values is
available as `SACTrace._header`.  Formatted non-null headers are viewable using
`print(sac)` or the `.lh()` or `listhdr()` methods.  Relative time headers and
picks are viewable with `lh('picks')`.


### Reference time and relative time header handling

The SAC reference time is built from "nz..." time fields in the header, and it
is available as the attribute `.reftime`, an ObsPy `UTCDateTime` instance.
`reftime` can be modified in two ways: by resetting it with a new absolute
`UTCDateTime` instance, or by adding/subtracting seconds from it.  **Modifying
the `reftime` will also modify all relative time headers such that they are
still correct in an absolute sense**.  This includes
`a`, `b`, `e`, `f`, `o`, and `t1`-`t9`.  This means that adjusting the
reference time does not invalidate the origin time, the first sample time, or
any picks!

Here, we build a 100-second `SACTrace` that starts at Y2K.

```python
sac = SACTrace(nzyear=2000, nzjday=1, nzhour=0, nzmin=0, nzsec=0, nzmsec=0,
               t1=23.5, data=numpy.arange(101))

sac.reftime
sac.b, sac.e, sac.t1
```

```
2000-01-01T00:00:00.000000Z
(0.0, 100.0, 23.5)
```

Move reference time by relative seconds, relative time headers are preserved.
```python
sac.reftime -= 2.5
sac.b, sac.e, sac.t1
```

```
(2.5, 102.5, 26.0)
```

Set reference time to new absolute time, two minutes later.  Relative time
 headers are preserved.
```python
sac.reftime = UTCDateTime(2000, 1, 1, 0, 2, 0, 0)
sac.b, sac.e
```

```
(-120.0, -20.0, -96.5)
```


