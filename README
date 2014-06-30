# CLD - Compact Language Detector

This package contains the CLD (Compact Language Detection) library as maintained by Dick Sites (https://code.google.com/p/cld2/). The first fork was done at revision r161. It also contains python bindings that were originally created by [Mike McCandless](http://code.google.com/p/chromium-compact-language-detector). The bindings here differ than upstream by making the full set of languages the default option supporting more than 165 languages!

The goal of this project is to consolidate the upstream library with its bindings, so the user can pip install one package instead of two.

The LICENSE is the same as Chromium's LICENSE and is included in the LICENSE file for reference.



## Python


### Installing

    $ git clone http://github.com/abosamoor/pycld2.git
    $ cd pycld2
    $ ./setup.py install

### Example

    import pycld2 as cld2

    detectedLangName, detectedLangCode, isReliable, textBytesFound, details = cld2.detect("This is my sample text", pickSummaryLanguage=True, removeWeakMatches=False)
    print '  detected: %s' % detectedLangName
    print '  reliable: %s' % (isReliable != 0)
    print '  textBytes: %s' % textBytesFound
    print '  details: %s' % str(details)

    # The output look lie so:
    #  detected: ENGLISH
    #  reliable: True
    #  textBytes: 25
    #  details: [('ENGLISH', 'en', 64, 20.25931928687196), ('FRENCH', 'fr', 36, 8.221993833504625)]

### Documentation

First, you must get your content (plain text or HTML) encoded into UTF8 bytes.  Then, detect like this:

    topLanguageName, topLanguageCode, isReliable, textBytesFound, details = cld2.detect(bytes)

The code and name of the top language is returned.  isReliable is True
if the top language is much better than 2nd best language.
textBytesFound tells you how many actual bytes CLD analyzed (after
removing HTML tags, collapsing areas of too-many-spaces, etc.).
details has an entry per top 3 languages that matched, that includes
the percent confidence of the match as well as a separate normalized
score.

The detect method takes optional params:

  * `isPlainText` (default is False): set to True if you know your bytes
    don't have any XML/HTML markup

  * `includeExtendedLanguages` (default is True): set to False to
    exclude "extended" languages added by Google

  * `hintTopLevelDomain` (default is None): set to the last part of the
    domain name that the content came from (for example if the URL was
    http://www.krasnahora.cz, pass the string 'cz').  This gives a
    hint that can bias the detector somewhat.

  * `hintLanguageCode` (default is None): set to the possible language.
    For example, if the web-server declared the language, or the
    content itself embedded an http-equiv meta tag declaring the
    language, pass this (for example, "it" for Italian).  This gives a
    hint that can bias the detector somewhat.

  * `hintEncoding` (default is None): set to the original encoding of
    the content (note you still must pass UTF-8 encoded bytes).  This
    gives a hint that can bias the detector somewhat.  NOTE: this is
    currently not working.

  * `pickSummaryLanguage` (default is False): if False, CLD will always
    return the top matching language as the answer.  If True, it will
    sometimes pick 2nd or 3rd match (for example, if English and X
    match, where X (not UNK) is big enough, assume the English is
    boilerplate and return X).  In simple testing accuracy seems to
    suffer a bit (XX to YY %) when this is True so I've defaulted to
    False.

  * `removeWeakMatches` (default is True): if a match isn't strong
    enough, delete it.  This ensures some amount of confidence when a
    language is returned.


The module exports these global constants:

  * `cld2.ENCODINGS`: list of the encoding names CLD recognizes (if you
    provide hintEncoding, it must be one of these names).

  * `cld2.LANGUAGES`: list of languages and their codes (if you provide
    hintLanguageCode, it must be one of the codes from these codes).

  * `cld2.EXTERNAL_LANGUAGES`: list of external languages and their
    codes.  Note that external languages cannot be hinted, but may be
    matched if you pass includeExtendedLanguages=True (the default).

  * `cld2.DETECTED_LANGUAGES`: list of all detectable languages, as best
    I can determine (this was reverse engineered from a unit test, ie
    it contains a language X if that language was tested and passes
    for at least one example text).
