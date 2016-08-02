#  coding: utf-8
"""
Detects languages in UTF-8 text, based largely on groups of four letters.

CLD2 probabilistically detects languages in Unicode UTF-8 text, either plain
text or HTML/XML. Legacy encodings must be converted to valid UTF-8 by the
caller. For mixed-language input, CLD2 returns the top three languages found
and their approximate percentages of the total text bytes (e.g. 80% English and
20% French out of 1000 bytes of text means about 800 bytes of English and 200
bytes of French). Optionally, it also returns a vector of text spans with the
language of each identified. This may be useful for applying different
spelling-correction dictionaries or different machine translation requests to
each span. The design target is web pages of at least 200 characters (about two
sentences); CLD2 is not designed to do well on very short text, lists of proper
names, part numbers, etc.

CLD2 is a Naïve Bayesian classifier, using one of three different token
algorithms:

- For Unicode scripts such as Greek and Thai that map one-to-one to detected
  languages, the script defines the result.
- For the 80,000+ character Han script and its CJK combination with Hiragana,
  Katakana, and Hangul scripts, single letters (unigrams) are scored.
- For all other scripts, sequences of four letters (quadgrams) are scored.

Scoring is done exclusively on lowercased Unicode letters and marks, after
expanding HTML entities &xyz; and after deleting digits, punctuation, and
<tags>. Quadgram word beginnings and endings (indicated here by underscore) are
explicitly used, so the word ``_look_`` scores differently from the
word-beginning ``_look`` or the mid-word ``look``. Quadgram single-letter
"words" are completely ignored. For each letter sequence, the scoring uses the
3-6 most likely languages and their quantized log probabilities. The training
corpus is manually constructed from chosen web pages for each language, then
augmented by careful automated scraping of over 100M additional web pages.

Several embellishments improve the basic algorithm: additional scoring of some
sequences of two CJK letters or eight other letters; scoring some words and
word pairs that are distinctive within sets of statistically-close languages
such as {Malay, Indonesian} or {Spanish, Portuguese, Galician}; removing
repetitive sequences/words that would otherwise skew the scoring, such as “jpg”
in “foo.jpg bar.jpg baz.jpg”; removing web-specific words that convey almost no
language information such as page, link, click, td, tr, copyright, wikipedia,
http.

Several hints can be supplied. Because these can be inaccurate on web pages,
they are just hints -- they add a bias but do not force a specific language to
be the detection result. The hints include expected language, original document
encoding, document URL top-level domain name, and embedded <…lang=xx …>
language tags.

The table-driven extraction of letter sequences and table-driven scoring is
highly optimized for both space and speed, running about 10x faster than other
detectors and covering over 70 languages in 1.8MB of x86 code and tables. The
main quadgram lookup table consists of 256K four-byte entries, covering about
50 languages. Detection over the average web page of 30KB (half
tags/digits/punctuation, half letters) takes roughly 1 msec on a current x86
processor.

Languages supported
====================
161 languages (175 language-script combinations)
Abkhazian, Afar, Afrikaans, Akan, Albanian, Amharic, Arabic, Armenian,
Assamese, Aymara Azerbaijani, Bashkir, Basque, Belarusian, Bengali, Bihari,
Bislama, Breton, Bulgarian Burmese, Catalan, Cebuano, Cherokee, Chinese,
Chinese_T, Corsican, Croatian, Czech Danish, Dhivehi, Dutch, Dzongkha, English,
Esperanto, Estonian, Faroese, Fijian, Finnish French, Frisian, Galician, Ganda,
Georgian, German, Greek, Greenlandic, Guarani Gujarati, Haitian_Creole, Hausa,
Hawaiian, Hebrew, Hindi, Hmong, Hungarian, Icelandic Igbo, Indonesian,
Interlingua, Interlingue, Inuktitut, Inupiak, Irish, Italian Japanese,
Javanese, Kannada, Kashmiri, Kazakh, Khasi, Khmer, Kinyarwanda, Klingon Korean,
Kurdish, Kyrgyz, Laothian, Latin, Latvian, Limbu, Lingala, Lithuanian
Luxembourgish, Macedonian, Malagasy, Malay, Malayalam, Maltese, Manx, Maori,
Marathi Mauritian_Creole, Mongolian, Nauru, Nepali, Norwegian, Norwegian_N,
Nyanja, Occitan Oriya, Oromo, Pashto, Pedi, Persian, Pig_Latin, Polish,
Portuguese, Punjabi, Quechua Rhaeto_Romance, Romanian, Rundi, Russian, Samoan,
Sango, Sanskrit, Scots, Scots_Gaelic Serbian, Seselwa, Sesotho, Shona, Sindhi,
Sinhalese, Siswant, Slovak, Slovenian, Somali Spanish, Sundanese, Swahili,
Swedish, Syriac, Tagalog, Tajik, Tamil, Tatar, Telugu, Thai Tibetan, Tigrinya,
Tonga, Tsonga, Tswana, Turkish, Turkmen, Uighur, Ukrainian, Urdu Uzbek, Venda,
Vietnamese, Volapuk, Waray_Philippines, Welsh, Wolof, Xhosa, Yiddish Yoruba,
Zhuang, Zulu

Plus text in these additional 65 Unicode-6.2 scripts
Avestan, Balinese, Bamum, Batak, Bopomofo, Brahmi, Braille, Buginese, Buhid,
Carian Chakma, Cham, Coptic, Cuneiform, Cypriot, Deseret, Egyptian_Hieroglyphs,
Glagolitic Gothic, Hanunoo, Imperial_Aramaic, Inscriptional_Pahlavi,
Inscriptional_Parthian Javanese, Kaithi, Kayah_Li, Kharoshthi, Lepcha,
Linear_B, Lisu, Lycian, Lydian, Mandaic Meetei_Mayek, Meroitic_Cursive,
Meroitic_Hieroglyphs, Miao, New_Tai_Lue, Nko, Ogham Ol_Chiki, Old_Italic,
Old_Persian, Old_South_Arabian, Old_Turkic, Osmanya, Phags_Pa Phoenician,
Rejang, Runic, Samaritan, Saurashtra, Sharada, Shavian, Sora_Sompeng
Syloti_Nagri, Tagbanwa, Tai_Le, Tai_Tham, Tai_Viet, Takri, Tifinagh, Ugaritic,
Vai, Yi

240 total language-script combinations

Caveats
=======
There are nine sets of statistically-close languages; CLD2 may interconfuse
them.

   {INDONESIAN MALAY}
   {DZONGKHA TIBETAN}
   {CZECH SLOVAK}
   {XHOSA ZULU}
   {CROATIAN SERBIAN}
   {BIHARI HINDI MARATHI NEPALI}
   {DANISH NORWEGIAN NORWEGIAN_N}
   {GALICIAN PORTUGUESE SPANISH}
   {KINYARWANDA RUNDI}

In addition, these ten languages are relatively recent additions and have not
be well-shaken-down: Akan, Cebuano, Hmong, Igbo, Mauritian_Creole, Nyanja,
Pedi, Seselwa, Venda, Waray_Philippines.
"""

from os.path import abspath, dirname, relpath
from os.path import join as joinpath
from collections import namedtuple
from cffi import FFI
import platform
import six


_DEBUG = False
_COMPILER_ARGS = ['-ggdb'] if _DEBUG else ['-O2']

# pylint: disable=invalid-name
_full_ffi = FFI()
_lite_ffi = FFI()
_pth = abspath(dirname(__file__))
_binding_decls = joinpath(_pth, 'binding_decls.h')
with open(_binding_decls) as bindings:
    declrs = bindings.read()
    _full_ffi.cdef(declrs)
    _lite_ffi.cdef(declrs)

_core_sources = [relpath(src) for src in [
    "cld2/encoding_lut.cc",
    "cld2/binding.cc",
    "cld2/internal/cldutil.cc",
    "cld2/internal/cldutil_shared.cc",
    "cld2/internal/compact_lang_det.cc",
    "cld2/internal/compact_lang_det_hint_code.cc",
    "cld2/internal/compact_lang_det_impl.cc",
    "cld2/internal/debug.cc",
    "cld2/internal/fixunicodevalue.cc",
    "cld2/internal/generated_entities.cc",
    "cld2/internal/generated_language.cc",
    "cld2/internal/generated_ulscript.cc",
    "cld2/internal/getonescriptspan.cc",
    "cld2/internal/lang_script.cc",
    "cld2/internal/offsetmap.cc",
    "cld2/internal/scoreonescriptspan.cc",
    "cld2/internal/tote.cc",
    "cld2/internal/utf8statetable.cc"]]

_full_table = [relpath(src) for src in [
    "cld2/internal/cld_generated_cjk_uni_prop_80.cc",
    "cld2/internal/cld2_generated_cjk_compatible.cc",
    "cld2/internal/cld_generated_cjk_delta_bi_32.cc",
    "cld2/internal/generated_distinct_bi_0.cc",
    "cld2/internal/cld2_generated_quad0122.cc",
    "cld2/internal/cld2_generated_deltaocta0122.cc",
    "cld2/internal/cld2_generated_distinctocta0122.cc",
    "cld2/internal/cld_generated_score_quad_octa_0122.cc"]]

_lite_table = [relpath(src) for src in [
    "cld2/internal/cld_generated_cjk_uni_prop_80.cc",
    "cld2/internal/cld2_generated_cjk_compatible.cc",
    "cld2/internal/cld_generated_cjk_delta_bi_4.cc",
    "cld2/internal/generated_distinct_bi_0.cc",
    "cld2/internal/cld2_generated_quadchrome_2.cc",
    "cld2/internal/cld2_generated_deltaoctachrome.cc",
    "cld2/internal/cld2_generated_distinctoctachrome.cc",
    "cld2/internal/cld_generated_score_quad_octa_2.cc"]]

_full_sources = _core_sources + _full_table
_lite_sources = _core_sources + _lite_table

_include_dirs = [relpath(inc) for inc in [
    "cld2/public", "cld2/internal", "cld2"]]

if platform.system() == 'Windows':
    _include_dirs.append(relpath("msinttypes"))

_full_cld2 = _full_ffi.verify('#include <binding_decls.h>',
                              sources=_full_sources,
                              include_dirs=_include_dirs,
                              extra_compile_args=_COMPILER_ARGS)

_lite_cld2 = _lite_ffi.verify('#include <binding_decls.h>',
                              sources=_lite_sources,
                              include_dirs=_include_dirs,
                              extra_compile_args=_COMPILER_ARGS)


def __establish_languages(ffi, cld):
    to_ret = []
    _lingus = cld.cld_languages()
    _codes = cld.cld_langcodes()

    for i in six.moves.xrange(cld.cld_num_languages()):
        lingus = ffi.string(_lingus[i])
        code = ffi.string(_codes[i])
        if lingus and not (lingus.isdigit() or lingus == b'Unknown'):
            to_ret.append((lingus, code))

    return tuple(sorted(to_ret, key=lambda x: x[0]))


def __establish_encodings(ffi, cld):
    to_ret = []
    _encodings = cld.cld_supported_encodings()
    for i in six.moves.xrange(cld.cld_num_encodings()):
        encoding = ffi.string(_encodings[i])
        if encoding and encoding != b'UNKNOWN_ENCODING':
            to_ret.append(encoding)
    return tuple(sorted(to_ret))


LANGUAGES = __establish_languages(_full_ffi, _full_cld2)
ENCODINGS = __establish_encodings(_full_ffi, _full_cld2)

Detections = namedtuple('Detections',
                        ['is_reliable', 'bytes_found', 'details'])
VectorDetections = namedtuple('DetailedDetections',
                              ['is_reliable', 'bytes_found', 'details',
                               'vectors'])
Detection = namedtuple('Detection',
                       ['language_name', 'language_code', 'percent', 'score'])
Vector = namedtuple('Vector',
                    ['offset', 'num_bytes', 'language_name', 'language_code'])

# pylint: disable=too-many-arguments,too-many-locals
def detect(utf8Bytes, isPlainText=True, hintTopLevelDomain=None,  # noqa
           hintLanguage=None, hintLanguageHTTPHeaders=None,
           hintEncoding=None, returnVectors=False,
           useFullLangTables=False,
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

    useFullLangTables : bool, optional
        If True, then use the full set of language tables currently available
        in CLD, otherwise use the restricted set

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
    `Detections(is_reliable, bytes_found, details)
    when `returnVectors` is False
    `Detections(is_reliable, bytes_found, details, vectors`
    when `returnVectors` is True

    isReliable : boolean
        is True if the detection is high confidence

    textBytesFound : int
        is the total number of bytes of text detected

    details : tuple of Detection
        A tuple of up to three detected languages, where each is a
        namedtuple of `(language_name, language_code, percent, score)`.

        `language_name` is the internal CLD2 name for the language.
        `language_code` is a ISO 639-1 lanuguage code.
        `percent` is what percentage of the original text was detected as.
        `score` is the confidence score for that language.

    vectors : tuple of Vector
        A tuple of detected languages segments, where each is a
        namedtuple of `(offset, num_bytes, language_name, language_code)`

        `offset` is where in the text the vector starts from.
        `num_bytes` is the number of bytes the vector extends to.
        `language_name` is the internal CLD2 name for the language.
        `language_code` is a ISO 639-1 lanuguage code.
    """

    cld2 = _full_cld2 if useFullLangTables else _lite_cld2
    ffi = _full_ffi if useFullLangTables else _lite_ffi

    if not utf8Bytes:
        utf8Bytes = ' '

    if six.PY3 and isinstance(utf8Bytes, str):
        utf8Bytes = utf8Bytes.encode('utf8')

    def __cstr_or_null(string):
        if not string:
            return ffi.NULL
        else:
            if six.PY3 and isinstance(string, str):
                return string.encode('ascii')
            else:
                return string

    cld_results = cld2.cld_create_results()  # noqa

    if cld_results == ffi.NULL or cld_results is None:
        raise MemoryError()

    try:
        hint_content_lang_box = __cstr_or_null(hintLanguageHTTPHeaders)
        hint_lang_box = __cstr_or_null(hintLanguage)
        hint_encoding_box = __cstr_or_null(hintEncoding)
        hint_tld_box = __cstr_or_null(hintTopLevelDomain)

        ret_code = cld2.cld_detect(utf8Bytes, len(utf8Bytes),  # noqa
                                   cld_results, hint_content_lang_box,
                                   hint_tld_box, hint_lang_box,
                                   hint_encoding_box, isPlainText,
                                   returnVectors, bestEffort,
                                   debugScoreAsQuads, debugHTML,
                                   debugCR, debugVerbose,
                                   debugQuiet, debugEcho)

        if ret_code == 1:
            raise ValueError("Unrecognized language hint name " +
                             "(got '%s'); " % hintLanguage +
                             "see cld.LANGUAGES for recognized language " +
                             "names (note that currently external languages " +
                             "cannot be hinted)")
        elif ret_code == 2:
            raise ValueError("Unrecognized encoding hint code " +
                             "(got '%s'); " % hintEncoding +
                             "see cld.ENCODINGS for recognized encodings")
        elif ret_code == 3:
            raise ValueError("input contains invalid UTF-8 around byte " +
                             "%d (of %d)" % (
                                 cld_results.valid_prefix_bytes,
                                 cld_results.bytes_found))
        elif ret_code != 0:
            raise ValueError("Unknown Error !")

        results = cld_results.results
        languages = [Detection(ffi.string(results[i].lang_name).decode('utf8'),
                               ffi.string(results[i].lang_code).decode('utf8'),
                               results[i].percent,
                               results[i].normalized_score)
                     for i in six.moves.xrange(3)]
        languages = tuple(languages)

        if returnVectors and cld_results.chunks is not ffi.NULL:
            vectors = []
            for idx in six.moves.xrange(cld_results.num_chunks):
                chunk = cld_results.chunks[idx]
                vectors.append(
                    Vector(chunk.offset,
                           chunk.bytes,
                           ffi.string(chunk.lang_name).decode('utf8'),
                           ffi.string(chunk.lang_code).decode('utf8'))
                )
            return VectorDetections(
                bool(cld_results.reliable),
                int(cld_results.bytes_found),
                languages,
                tuple(vectors)
            )
        else:
            return Detections(
                bool(cld_results.reliable),
                int(cld_results.bytes_found),
                languages,
            )
    finally:
        cld2.cld_destroy_results(cld_results)  # noqa
