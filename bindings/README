Dick Sites (and others) at Google graciously provided a new version
2.0 of the compact language detector, here:

  https://code.google.com/p/cld2/

and I (lucene@mikemccandless.com) created the Python bindings and
ported the C++ test case to test.py.

This has been tested on Ubuntu 14.04, with both Python 2.7.6 and
3.4.0.

Updated Nov 11 2014 to the latest CLD2 release, adding new bestEffort
flag (to force a guess even when confidence is low), and cutting over
to the CLD2 methods that confirm incoming UTF-8 is valid.

To build:

  * First checkout cld2, cd internal, run compile_libs.sh.  This will
    create both libcld2.so (small tables, detects 83 languages) and
    libcld2_full.so (large tables, detects 163 languages).  Install
    those libraries somewhere on your LD_LIBRARY_PATH, for example
    copy them into /usr/lib.

  * Edit both setup.py and setup_full.py: change CLD2_PATH to point to
    where you checked out the CLD2 sources.

  * python setup.py build

  * python setup_full.py build

Note that all Python sources work with both python 2.x and 3.x so if
you want to install for python3.x just repeat the above steps using
python3 (or whatever python command runs python 3.x in your
environment).

To test both the small and full language tables:

  * python test.py

The test produces a lot of output, due to the test cases testing the
debug flags; this is normal.  As long as it says OK in the end then
the tests passed.

To install:

  * python setup.py install (as root)

  * python setup_full.py install (as root)

For documentation run:

  * python -c "import cld2; help(cld2.detect)"

NOTE: gen_test.py and gen_enc.py were used as temporary helpers during
development and are not needed for building

NOTE: you must pass only valid UTF-8 bytes to the detect function,
otherwise you can hit segmentation fault or get incorrect results.
