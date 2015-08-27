## Relationship to ObsPy

PySAC is largely re-written from the
[obspy.io.sac](https://github.com/obspy/obspy/tree/master/obspy/io/sac) module,
with the intention of eventually replacing it.

## Why a re-write?

The sacio module underlying ObsPy's SAC handling was sometimes hard to follow,
as it has a long inheritance, which made it hard to track down issues or make
fixes. This re-write attempts to make the SAC plugin easier to understand and
maintain, as well as offer some potential improvements.

## Improve maintainability.

I've split out the header specification (header.py), the low-level array-based
SAC file I/O (arrayio.py), and the object-oriented interface (sactrace.py),
whereas it was previously all within one sacio.py module. I hope that the flow
of how each plugs into the other is clear, so that bug tracking is
straight-forward, and that hacking on one aspect of SAC handling is not
cluttered/distracted by another.

## Expand support for round-trip SAC file processing

This rewrite attempts to improve support for a common work flow: read one or
more SAC files into ObsPy, do some processing, then (over)write them back as
SAC files that look mostly like the originals. Previously, ObsPy Traces written
to SAC files wrote only files based on the first sample time (iztype 9/'ib').
In `util.py:obspy_to_sac_header` of this module, if an old tr.stats.sac SAC
header is found, the iztype and reference "nz" times are used and kept, and the
"b" and "e" times of the Trace being written are adjusted according to this
reference time. This preserves the absolute reference of any relative time
headers, like t0-t9, carried from the old SAC header into the new file. This
can only be done if SAC to Trace conversion preserves these "nz" time headers,
which is possible with the current `debug_headers=True` flag.
