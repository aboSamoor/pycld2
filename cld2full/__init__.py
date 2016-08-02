from cld2 import detect as _detect

def detect(utf8Bytes, isPlainText=True, hintTopLevelDomain=None,  # noqa
           hintLanguage=None, hintLanguageHTTPHeaders=None,
           hintEncoding=None, returnVectors=False,
           bestEffort=False,
           debugScoreAsQuads=False, debugHTML=False,
           debugCR=False, debugVerbose=False, debugQuiet=False,
           debugEcho=False):
    """
    Detect language(s) from a UTF8 string.

    Parameters
    ----------
    utf8Bytes : unicode
        The text to detect, encoded as UTF-8 bytes (required).  If this is not
        valid UTF-8, then an ValueError is raised.

    isPlainText : bool, optional
        If False, then the input is HTML and CLD will skip HTML tags, expand
        HTML entities, detect HTML <lang ...> tags, etc.

    hintTopLevelDomain : str, optional
        E.g., 'id' boosts Indonesian

    hintLanguage : str, optional
        E.g., 'ITALIAN' or 'it' boosts Italian; see `cld.LANGUAGES` for all
        known language

    hintLanguageHTTPHeaders : str, optional
        E.g., 'mi,en' boosts Maori and English

    hintEncoding : str, optional
        E.g, 'SJS' boosts Japanese; see `cld.ENCODINGS` for all known encodings

    returnVectors : bool, optional
        If True then the vectors indicating which language was detected in
        which byte range are returned in addition to details.  The vectors are
        a sequence of `(bytesOffset, bytesLength, languageName, languageCode)`,
        in order.  `bytesOffset` is the start of the vector, `bytesLength` is
        the length of the vector.  Note that there is some added CPU cost if
        this is True.

    debugScoreAsQuads : bool, optional
        Normally, several languages are detected solely by their Unicode
        script.  Combined with appropriate lookup tables, this flag forces
        them instead to be detected via quadgrams. This can be a useful
        refinement when looking for meaningful text in these languages, instead
        of just character sets.  The default tables do not support this use.

    debugHTML : bool, optional
        For each detection call, write an HTML file to `stderr`, showing the
        text chunks and their detected languages. See
        `docs/InterpretingCLD2UnitTestOutput.pdf` to interpret this output.

    bestEffort : bool, optional
        If True then allow low-quality results for short text, rather than
        forcing the result to UNKNOWN_LANGUAGE.  This may be of use for those
        desiring approximate results on short input text, but there is no claim
        that these result are very good.

    debugCR : bool, optional
        In that HTML file, force a new line for each chunk.

    debugVerbose : bool, optional
        In that HTML file, show every lookup entry.

    debugQuiet : bool, optional
        In that HTML file, suppress most of the output detail.

    debugEcho : bool, optional
        Echo every input buffer to `stderr`.

    Returns
    -------
    `(isReliable, textBytesFound, details) when `returnVectors` is False
    `(isReliable, textBytesFound, details, vectors` when `returnVectors` is
    True

    isReliable : boolean
        is True if the detection is high confidence

    textBytesFound : int
        is the total number of bytes of text detected

    details : tuple
        is a tuple of up to three detected languages, where each is
        tuple is `(languageName, languageCode, percent, score)`.  `Percent` is
        what percentage of the original text was detected as this language
        and `score` is the confidence score for that language.
    """
    return _detect(utf8Bytes, isPlainText=isPlainText,
                   hintTopLevelDomain=hintTopLevelDomain,
                   hintLanguage=hintLanguage,
                   hintLanguageHTTPHeaders=hintLanguageHTTPHeaders,
                   hintEncoding=hintEncoding, returnVectors=returnVectors,
                   bestEffort=bestEffort,
                   debugScoreAsQuads=debugScoreAsQuads,
                   debugHTML=debugHTML,
                   debugCR=debugCR,
                   debugVerbose=debugVerbose,
                   debugQuiet=debugQuiet,
                   debugEcho=debugEcho,
                   useFullLangTables=True)
