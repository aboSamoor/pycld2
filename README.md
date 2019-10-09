# PYCLD2 - Python Bindings to CLD2

Python bindings for the Compact Langauge Detect 2 (CLD2).

[![Downloads](https://img.shields.io/pypi/dm/pycld2.svg)](https://pypi.python.org/pypi/pycld2)
[![Latest version](https://img.shields.io/pypi/v/pycld2.svg)](https://pypi.python.org/pypi/pycld2)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pycld2.svg)](https://pypi.python.org/pypi/pycld2)
[![Development Status](https://img.shields.io/pypi/status/pycld2.svg)](https://pypi.python.org/pypi/pycld2)
[![Download format](https://img.shields.io/pypi/format/pycld2.svg)](https://pypi.python.org/pypi/pycld2)
[![Build status](https://travis-ci.org/aboSamoor/pycld2.png?branch=master)](https://travis-ci.org/aboSamoor/pycld2)

This package contains forks of:

- The [`cld2` C++ library](https://github.com/CLD2Owners/cld2), developed by Dick Sites
- The [`chromium-compact-language-detector` C++ extension module](https://github.com/mikemccand/chromium-compact-language-detector),
  originally created by Mike McCandless, which has been modified post-fork.
  These bindings, among other changes, make the support of over 165 languages
  the default.

The goal of this project is to consolidate the upstream library with its bindings, so the user can `pip install` one package instead of two.

The LICENSE is the same as Chromium's LICENSE and is included in the
LICENSE file for reference.

## Installing

```bash
$ python -m pip install -U pycld2
```

## Example

```python
import pycld2 as cld2

isReliable, textBytesFound, details = cld2.detect(
    "а неправильный формат идентификатора дн назад"
)

print(isReliable)
# True
details[0]
# ('RUSSIAN', 'ru', 98, 404.0)

fr_en_Latn = """\
France is the largest country in Western Europe and the third-largest in Europe as a whole.
A accès aux chiens et aux frontaux qui lui ont été il peut consulter et modifier ses collections
et exporter Cet article concerne le pays européen aujourd’hui appelé République française.
Pour d’autres usages du nom France, Pour une aide rapide et effective, veuiller trouver votre aide
dans le menu ci-dessus.
Motoring events began soon after the construction of the first successful gasoline-fueled automobiles.
The quick brown fox jumped over the lazy dog."""

isReliable, textBytesFound, details, vectors = cld2.detect(
    fr_en_Latn, returnVectors=True
)
print(vectors)
# ((0, 94, 'ENGLISH', 'en'), (94, 329, 'FRENCH', 'fr'), (423, 139, 'ENGLISH', 'en'))
```

## API

This package exports one function, `detect()`. See `help(detect)` for the full docstring.

The first parameter (`utf8Bytes`) is the text for which you want to detect language.

`utf8Bytes` may be either:

- `str` (example: `"¼ cup of flour"`)
- `bytes` that have been encoded using UTF-8 (example: `"¼ cup of flour".encode("utf-8")`)

Bytes that are *not* UTF-8 encoded will raise a `pycld2.error`.  For example, passing
b"\xbc cup of flour" (which is `"¼ cup of flour".encode("latin-1")`) will raise.

All other parameters are optional:

| Parameter | Type/Default | Use |
| --------- | ------------ | --- |
| `utf8Bytes` | `str` or `bytes`\* | The text to detect language for. |
| `isPlainText` | `bool`, default `False` | If `False`, then the input is HTML and CLD will skip HTML tags, expand HTML entities, detect HTML `<lang ...>` tags, etc. |
| `hintTopLevelDomain` | `str` | E.g., `'id'` boosts Indonesian. |
| `hintLanguage` | `str` | E.g., `'ITALIAN'` or `'it'` boosts Italian; see `cld.LANGUAGES` for all known languages. |
| `hintLanguageHTTPHeaders` | `str` | E.g., `'mi,en'` boosts Maori and English. |
| `hintEncoding` | `str` | E.g, `'SJS'` boosts Japanese; see `cld.ENCODINGS` for all known encodings. |
| `returnVectors` |  `bool`, default `False` | If `True`, then the vectors indicating which language was detected in which byte range are returned in addition to details.  The vectors are a sequence of `(bytesOffset, bytesLength, languageName, languageCode)`, in order. `bytesOffset` is the start of the vector, `bytesLength `is the length of the vector.  Note that there is some added CPU cost if this is True.  (Approx. 2x performance hit.) |
| `debugScoreAsQuads` | `bool`, default `False` | Normally, several languages are detected solely by their Unicode script.  Combined with appropritate lookup tables, this flag forces them instead to be detected via quadgrams. This can be a useful refinement when looking for meaningful text in these languages, instead of just character sets. The default tables do not support this use. |
| `debugHTML` | `bool`, default `False` | For each detection call, write an HTML file to stderr, showing the text chunks and their detected languages. See `cld2/docs/InterpretingCLD2UnitTestOutput.pdf` to interpret this output. |
| `debugCR` | `bool`, default `False` | In that HTML file, force a new line for each chunk. |
| `debugVerbose` | `bool`, default `False` | In that HTML file, show every lookup entry. |
| `debugQuiet` | `bool`, default `False` | In that HTML file, suppress most of the output detail. |
| `debugEcho` | `bool`, default `False` | Echo every input buffer to stderr. |
| `bestEffort` | `bool`, default `False` | If `True`, then allow low-quality results for short text, rather than forcing the result to `"UNKNOWN_LANGUAGE"`.  This may be of use for those desiring approximate results on short input text, but there is no claim that these result are very good. |

<sup>\*If `bytes`, must be UTF-8 encoded bytes.</sup>

## Constants

This package exports these global constants:

| Constant | Description |
| -------- | ----------- |
| `pycld2.ENCODINGS` | list of the encoding names CLD recognizes (if you provide `hintEncoding`, it must be one of these names). |
| `pycld2.LANGUAGES` | list of languages and their codes (if you provide `hintLanguageCode`, it must be one of the codes from these codes). |
| `pycld2.EXTERNAL_LANGUAGES` | list of external languages and their codes. |
| `pycld2.DETECTED_LANGUAGES` | list of all detectable languages. |
