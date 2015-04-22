CLD2-CFFI - Python (CFFI) Bindings for Compact Language Detector 2
==================================================================

`CFFI <cffi.readthedocs.org>`_ bindings for CLD2

-----

|pypi| |build| |coverage| |lint|

-----


This package contains the CLD (Compact Language Detection) library as
maintained by Dick Sites (https://code.google.com/p/cld2/). The first
fork was done at revision r161. It also contains python bindings that
were originally created by `Mike
McCandless <http://code.google.com/p/chromium-compact-language-detector>`_.
The bindings have gone through several hands, with the latest changes being made
to rework the bindings for `CFFI <cffi.readthedocs.org>`_.

These bindings are identical in API to the original cld2 bindings, and as a
result can be used as a drop in replacement.

The LICENSE_ is the same as Chromium's LICENSE and is included in the
LICENSE_ file for reference.

==========
Installing
==========

Should be as simple as

.. code-block:: bash

   $ pip install cld2-cffi

-------------------
Development Version
-------------------

The **latest development version** can be installed directly from GitHub:

.. code-block:: bash

    $ pip install --upgrade 'git+https://github.com/GregBowyer/cld2-cffi.git'

=====
Usage
=====

.. code-block:: python

    import cld2

    detectedLangCode, isReliable, textBytesFound, details = \
        cld2.detect("This is my sample text", pickSummaryLanguage=True, removeWeakMatches=False)
    print '  reliable: %s' % (isReliable != 0)
    print '  textBytes: %s' % textBytesFound
    print '  details: %s' % str(details)

    # The output look like so:
    #  reliable: True
    #  textBytes: 25
    #  details: [('ENGLISH', 'en', 64, 20.25931928687196), ('FRENCH', 'fr', 36, 8.221993833504625)]

=============
Documentation
=============

First, you must get your content (plain text or HTML) encoded into UTF8
bytes. Then, detect like this:

.. code-block:: python

    isReliable, textBytesFound, details = cld2.detect(bytes)

``isReliable`` 
    is True if the top language is much better than 2nd best language.

``textBytesFound`` 
    tells you how many actual bytes CLD analyzed (after removing HTML tags,
    collapsing areas of too-many-spaces, etc.).  

``details`` 
    has an entry per top 3 languages that matched, that includes the percent
    confidence of the match as well as a separate normalized score.

The module exports these global constants:

``cld2.ENCODINGS``
    list of the encoding names CLD recognizes (if you provide hintEncoding, it
    must be one of these names).

``cld2.LANGUAGES``
    list of languages and their codes (if you provide hintLanguageCode, it must
    be one of the codes from these codes).

``cld2.EXTERNAL_LANGUAGES``
    list of external languages and their codes. Note that external languages
    cannot be hinted, but may be matched if you pass
    ``includeExtendedLanguages=True`` (the default).

``cld2.DETECTED_LANGUAGES``
    list of all detectable languages, as best I can determine (this was reverse
    engineered from a unit test, ie it contains a language X if that language
    was tested and passes for at least one example text).


=======
Authors
=======

Please see `AUTHORS <https://github.com/GregBowyer/cld2-cffi/blob/master/BUG_REPORTS.rst>`_.


==============
Reporting bugs
==============
Please see `BUG_REPORTS <https://github.com/GregBowyer/cld2-cffi/blob/master/BUG_REPORTS.rst>`_.


==========
Contribute
==========

Please see `CONTRIBUTING <https://github.com/GregBowyer/cld2-cffi/blob/master/CONTRIBUTING.rst>`_.


=======
Licence
=======

Please see LICENSE_.

.. _LICENSE: https://github.com/GregBowyer/cld2-cffi/blob/master/LICENSE

.. |pypi| image:: https://img.shields.io/pypi/v/cld2-cffi.svg?style=flat-square&label=latest%20version
    :target: https://pypi.python.org/pypi/cld2-cffi
    :alt: Latest version released on PyPi

.. |build| image:: https://img.shields.io/travis/GregBowyer/cld2-cffi/master.svg?style=flat-square&label=build
    :target: http://travis-ci.org/GregBowyer/cld2-cffi
    :alt: Build status 

.. |coverage| image:: https://img.shields.io/codecov/c/github/GregBowyer/cld2-cffi.svg
    :target: https://codecov.io/github/GregBowyer/cld2-cffi
    :alt: Coverage

.. |lint| image:: https://landscape.io/github/GregBowyer/cld2-cffi/master/landscape.svg?style=flat-square
   :target: https://landscape.io/github/GregBowyer/cld2-cffi/master
   :alt: Code Health
