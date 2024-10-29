//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h> // Windows compat (vs. strings.h)

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

// From ../cld2/public/
#include "compact_lang_det.h"
#include "encodings.h"

// From ../cld2/internal/
#include "lang_script.h"

// The version of the Python bindings, which gets set to _pycld2.__version__.
// For a version of CLD2 itself, see CLD2::DetectLanguageVersion().
#define PYCLD2_VERSION "0.42"

// Implementation is in ./encodings.cc
CLD2::Encoding EncodingFromName(const char *name);

struct cld_encoding {
  const char *name;
  CLD2::Encoding encoding;
};

extern const cld_encoding cld_encoding_info[];
namespace CLD2 {
  extern const int kNameToLanguageSize;
  extern const CharIntPair kNameToLanguage[];
}

struct PYCLDState {
  PyObject *error;
};

#ifdef IS_PY3K
#define GETSTATE(m) ((struct PYCLDState*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct PYCLDState _state;
#endif

static PyObject *
detect(PyObject *self, PyObject *args, PyObject *kwArgs)
{
  const char *bytes;

  CLD2::CLDHints cldHints;
  cldHints.tld_hint = 0;
  cldHints.content_language_hint = 0;

  int isPlainText = 0;
  const char *hintLanguage = 0;
  const char *hintEncoding = 0;

  int returnVectors = 0;

  int flagScoreAsQuads = 0;
  int flagHTML = 0;
  int flagCR = 0;
  int flagVerbose = 0;
  int flagQuiet = 0;
  int flagEcho = 0;
  int flagBestEffort = 0;

  static const char *kwList[] = {
    "utf8Bytes", "isPlainText", "hintTopLevelDomain", "hintLanguage",
    "hintLanguageHTTPHeaders", "hintEncoding", "returnVectors",
    "debugScoreAsQuads", "debugHTML", "debugCR", "debugVerbose",
    "debugQuiet", "debugEcho", "bestEffort", NULL
  };

  if (!PyArg_ParseTupleAndKeywords(args,
                                   kwArgs,
                                   "s|izzzziiiiiiii",
                                   (char **) kwList,
                                   &bytes,
                                   &numBytes,
                                   &isPlainText,
                                   &cldHints.tld_hint,
                                   &hintLanguage,
                                   &cldHints.content_language_hint,
                                   &hintEncoding,
                                   &returnVectors,
                                   &flagScoreAsQuads,
                                   &flagHTML,
                                   &flagCR,
                                   &flagVerbose,
                                   &flagQuiet,
                                   &flagEcho,
                                   &flagBestEffort)) {
    return NULL;
  }
  int numBytes = strlen(bytes);
  
  int flags = 0;
  if (flagScoreAsQuads != 0) {
    flags |= CLD2::kCLDFlagScoreAsQuads;
  }
  if (flagHTML != 0) {
    flags |= CLD2::kCLDFlagHtml;
  }
  if (flagCR != 0) {
    flags |= CLD2::kCLDFlagCr;
  }
  if (flagVerbose != 0) {
    flags |= CLD2::kCLDFlagVerbose;
  }
  if (flagQuiet != 0) {
    flags |= CLD2::kCLDFlagQuiet;
  }
  if (flagEcho != 0) {
    flags |= CLD2::kCLDFlagEcho;
  }
  if (flagBestEffort != 0) {
    flags |= CLD2::kCLDFlagBestEffort;
  }

  PyObject *CLDError = GETSTATE(self)->error;

  if (hintLanguage == 0) {
    cldHints.language_hint = CLD2::UNKNOWN_LANGUAGE;
  }
  else {
    cldHints.language_hint = CLD2::GetLanguageFromName(hintLanguage);
    if (cldHints.language_hint == CLD2::UNKNOWN_LANGUAGE) {
      PyErr_Format(CLDError,
                      "Unrecognized language hint '%s' not in cld.LANGUAGES",
                      hintLanguage);
      return NULL;
    }
  }

  if (hintEncoding == 0) {
    cldHints.encoding_hint = CLD2::UNKNOWN_ENCODING;
  }
  else {
    cldHints.encoding_hint = EncodingFromName(hintEncoding);
    if (cldHints.encoding_hint == CLD2::UNKNOWN_ENCODING) {
      PyErr_Format(CLDError,
                   "Unrecognized encoding hint '%s' not in cld.ENCODINGS",
                   hintEncoding);
      return NULL;
    }
  }

  bool isReliable;
  CLD2::Language language3[3];
  int percent3[3];
  double normalized_score3[3];
  int textBytesFound;
  int validPrefixBytes;
  CLD2::ResultChunkVector resultChunkVector;

  Py_BEGIN_ALLOW_THREADS
  CLD2::ExtDetectLanguageSummaryCheckUTF8(bytes,
                                          numBytes,
                                          isPlainText != 0,
                                          &cldHints,
                                          flags,
                                          language3,
                                          percent3,
                                          normalized_score3,
                                          returnVectors != 0 ? &resultChunkVector : 0,
                                          &textBytesFound,
                                          &isReliable,
                                          &validPrefixBytes);
  Py_END_ALLOW_THREADS

  if (validPrefixBytes < numBytes) {
    PyErr_Format(CLDError,
                 "input contains invalid UTF-8 around byte %d (of %d)",
                 validPrefixBytes,
                 numBytes);
    return NULL;
  }

  PyObject *details = PyTuple_New(3);
  for (Py_ssize_t idx = 0; idx < 3; idx++) {
    CLD2::Language lang = language3[idx];
    // Steals ref
    PyTuple_SET_ITEM(details,
                     idx,
                     Py_BuildValue("(ssif)",
                                   CLD2::LanguageName(lang),
                                   CLD2::LanguageCode(lang),
                                   percent3[idx],
                                   normalized_score3[idx]));
  }

  PyObject *result;

  if (returnVectors != 0) {
    PyObject *resultChunks = PyTuple_New(resultChunkVector.size());
    for (Py_ssize_t i = 0; i < resultChunkVector.size(); i++) {
      CLD2::ResultChunk chunk = resultChunkVector.at(i);
      CLD2::Language lang = static_cast<CLD2::Language>(chunk.lang1);
      // Steals ref
      PyTuple_SET_ITEM(resultChunks,
                       i,
                       Py_BuildValue("(iiss)",
                                     chunk.offset,
                                     chunk.bytes,
                                     CLD2::LanguageName(lang),
                                     CLD2::LanguageCode(lang)));
    }
    result = Py_BuildValue("(OiOO)",
                           isReliable ? Py_True : Py_False,
                           textBytesFound,
                           details,
                           resultChunks);
  }
  else {
    result = Py_BuildValue("(OiO)",
                           isReliable ? Py_True : Py_False,
                           textBytesFound,
                           details);
  }

  Py_DECREF(details);
  return result;
}

PyDoc_STRVAR(detect_doc,
"Detect language from str or UTF-8 encoded bytes.\n\
\n\
Arguments:\n\
\n\
    utf8Bytes: str or UTF-8 encoded bytes\n\
        The text to detect.  If this is not valid UTF-8, then a cld2.error is\n\
        raised.\n\
\n\
    isPlainText: bool, default False\n\
        If False, then the input is HTML and CLD will skip HTML tags,\n\
        expand HTML entities, detect HTML <lang ...> tags, etc.\n\
\n\
    hintTopLevelDomain: str\n\
        E.g., 'id' boosts Indonesian.\n\
\n\
    hintLanguage: str\n\
        E.g., 'ITALIAN' or 'it' boosts Italian; see cld.LANGUAGES for all\n\
        known languages.\n\
\n\
    hintLanguageHTTPHeaders: str\n\
        E.g., 'mi,en' boosts Maori and English.\n\
\n\
    hintEncoding: str\n\
        E.g, 'SJS' boosts Japanese; see cld.ENCODINGS for all known\n\
        encodings.\n\
\n\
    returnVectors:  bool, default False\n\
        If True, then the vectors indicating which language was detected in\n\
        which byte range are returned in addition to details.  The vectors are\n\
        a sequence of (bytesOffset, bytesLength, languageName, languageCode),\n\
        in order. bytesOffset is the start of the vector, bytesLength is the\n\
        length of the vector.  Note that there is some added CPU cost if this\n\
        is True.  (Approx. 2x performance hit.)\n\
\n\
    debugScoreAsQuads: bool, default False\n\
        Normally, several languages are detected solely by their Unicode\n\
        script.  Combined with appropritate lookup tables, this flag forces\n\
        them instead to be detected via quadgrams. This can be a useful\n\
        refinement when looking for meaningful text in these languages,\n\
        instead of just character sets. The default tables do not support\n\
        this use.\n\
\n\
    debugHTML: bool, default False\n\
        For each detection call, write an HTML file to stderr, showing the\n\
        text chunks and their detected languages.\n\
        See docs/InterpretingCLD2UnitTestOutput.pdf to interpret this output.\n\
\n\
    debugCR: bool, default False\n\
        In that HTML file, force a new line for each chunk.\n\
\n\
    debugVerbose: bool, default False\n\
        In that HTML file, show every lookup entry.\n\
\n\
    debugQuiet: bool, default False\n\
        In that HTML file, suppress most of the output detail.\n\
\n\
    debugEcho: bool, default False\n\
        Echo every input buffer to stderr.\n\
\n\
    bestEffort: bool, default False\n\
        If True, then allow low-quality results for short text, rather than\n\
        forcing the result to UNKNOWN_LANGUAGE.  This may be of use for\n\
        those desiring approximate results on short input text, but there\n\
        is no claim that these result are very good.\n\
\n\
  Returns: tuple\n\
\n\
    If returnVectors is False:\n\
\n\
        (isReliable, textBytesFound, details)\n\
\n\
    If returnVectors is True:\n\
\n\
        (isReliable, textBytesFound, details, vectors)\n\
\n\
    Where:\n\
\n\
    isReliable: bool\n\
        True if the detection is high confidence.\n\
\n\
    textBytesFound: int\n\
        Total number of bytes of text detected.\n\
\n\
    details: tuple\n\
        Tuple of up to three detected languages, where each is\n\
        tuple is (languageName, languageCode, percent, score).  percent is\n\
        what percentage of the original text was detected as this language\n\
        and score is the confidence score for that language.\n\
\n\
    vectors: tuple\n\
        Vectors indicating which language was detected in which byte range.\n\
");

static PyMethodDef CLDMethods[] = {
  {"detect", (PyCFunction)detect, METH_VARARGS|METH_KEYWORDS, detect_doc},
  {NULL, NULL, 0, NULL}  // Sentinel
};

#ifdef IS_PY3K

static int cld_traverse(PyObject *m, visitproc visit, void *arg) {
  Py_VISIT(GETSTATE(m)->error);
  return 0;
}

static int cld_clear(PyObject *m) {
  Py_CLEAR(GETSTATE(m)->error);
  return 0;
}

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,                    // m_base
  "cld",                                    // m_name
  NULL,                                     // m_doc
  sizeof(struct PYCLDState),                // m_size
  CLDMethods,                               // m_methods
  NULL,                                     // m_slots
  cld_traverse,                             // m_traverse
  cld_clear,                                // m_clear
  NULL                                      // m_free
};

#define INITERROR return NULL

// In Python 3, initialization function must be named PyInit_name(),
// where 'name' is the name of the module, hence this module will be named.
// stdlib does the same thing, such as PyInit__heapq for _heapq.
// _pycld2.
PyMODINIT_FUNC
PyInit__pycld2(void)

#else  // IS_PY3K

#define INITERROR return

PyMODINIT_FUNC
init_pycld2()
#endif
{
#ifdef IS_PY3K
  PyObject *m = PyModule_Create(&moduledef);
#else
  PyObject* m = Py_InitModule("_pycld2", CLDMethods);
#endif

  if (m == NULL) {
    INITERROR;
  }

  struct PYCLDState *st = GETSTATE(m);

  // Python name for the exception is 'pycld2.error'
  st->error = PyErr_NewException("pycld2.error", NULL, NULL);
  if (st->error == NULL) {
    Py_DECREF(m);
    INITERROR;
  }

  // Set module-global ENCODINGS tuple
  PyObject* pyEncs = PyTuple_New(CLD2::NUM_ENCODINGS - 1);
  // Steals ref:
  PyModule_AddObject(m, "ENCODINGS", pyEncs);
  unsigned int upto = 0;
  for (Py_ssize_t encIDX = 0; encIDX < CLD2::NUM_ENCODINGS; encIDX++) {
    if (static_cast<CLD2::Encoding>(encIDX) != CLD2::UNKNOWN_ENCODING) {
      if (upto == PyTuple_Size(pyEncs)) {
        PyErr_SetString(st->error, "failed to initialize cld.ENCODINGS");
        INITERROR;
      }
      PyTuple_SET_ITEM(pyEncs,
                       upto++,
                       PyUnicode_FromString(cld_encoding_info[encIDX].name));
    }
  }

  if (upto != PyTuple_Size(pyEncs)) {
    PyErr_SetString(st->error, "failed to initialize cld.ENCODINGS");
    INITERROR;
  }

  // Set module-global LANGUAGES tuple
  PyObject* pyLangs = PyTuple_New(CLD2::kNameToLanguageSize - 1);
  // Steals ref:
  PyModule_AddObject(m, "LANGUAGES", pyLangs);
  upto = 0;
  for (Py_ssize_t i = 0; i < CLD2::kNameToLanguageSize; i++) {
    const char *name = CLD2::kNameToLanguage[i].s;
    if (strcmp(name, "Unknown")) {
      if (upto == PyTuple_Size(pyLangs)) {
        PyErr_SetString(st->error, "failed to initialize cld.LANGUAGES");
        INITERROR;
      }
      CLD2::Language lang = CLD2::GetLanguageFromName(name);
      if (lang == CLD2::UNKNOWN_LANGUAGE) {
        PyErr_SetString(st->error, "failed to initialize cld.LANGUAGES");
        INITERROR;
      }
      // Steals ref
      PyTuple_SET_ITEM(pyLangs,
                       upto++,
                       Py_BuildValue("(zz)",
                                     LanguageName(lang),
                                     LanguageCode(lang)));
    }
  }

  if (upto != PyTuple_Size(pyLangs)) {
    PyErr_SetString(st->error, "failed to initialize cld.LANGUAGES");
    INITERROR;
  }

// VERSION is the C lib version, such as 'V2.0 - 20140204'
#ifdef IS_PY3K
  // Steals ref
  PyModule_AddObject(m,
                     "VERSION",
                     PyUnicode_FromString(CLD2::DetectLanguageVersion()));
#else
  // Steals ref
  PyModule_AddObject(m,
                     "VERSION",
                     PyString_FromString(CLD2::DetectLanguageVersion()));

#endif
  PyModule_AddStringConstant(m, "__version__", PYCLD2_VERSION);

  // Set module-global DETECTED_LANGUAGES tuple
  upto = 0;
  PyObject* detLangs = PyTuple_New(165);
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ABKHAZIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AFAR"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AFRIKAANS"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AKAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ALBANIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AMHARIC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ARABIC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ARMENIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ASSAMESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AYMARA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("AZERBAIJANI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BASHKIR"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BASQUE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BELARUSIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BENGALI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BIHARI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BISLAMA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BOSNIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BRETON"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BULGARIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("BURMESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CATALAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CEBUANO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CHEROKEE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CORSICAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CROATIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("CZECH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("Chinese"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ChineseT"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("DANISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("DHIVEHI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("DUTCH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("DZONGKHA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ENGLISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ESPERANTO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ESTONIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("FAROESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("FIJIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("FINNISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("FRENCH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("FRISIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GALICIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GANDA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GEORGIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GERMAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GREEK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GREENLANDIC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GUARANI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("GUJARATI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HAITIAN_CREOLE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HAUSA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HAWAIIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HEBREW"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HINDI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HMONG"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("HUNGARIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ICELANDIC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("IGBO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("INDONESIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("INTERLINGUA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("INTERLINGUE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("INUKTITUT"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("INUPIAK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("IRISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ITALIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("JAVANESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("Japanese"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KANNADA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KASHMIRI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KAZAKH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KHASI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KHMER"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KINYARWANDA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KURDISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("KYRGYZ"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("Korean"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LAOTHIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LATIN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LATVIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LIMBU"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LINGALA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LITHUANIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("LUXEMBOURGISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MACEDONIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MALAGASY"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MALAY"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MALAYALAM"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MALTESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MANX"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MAORI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MARATHI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MAURITIAN_CREOLE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("MONGOLIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NAURU"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NDEBELE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NEPALI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NORWEGIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NORWEGIAN_N"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("NYANJA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("OCCITAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ORIYA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("OROMO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("PASHTO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("PEDI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("PERSIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("POLISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("PORTUGUESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("PUNJABI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("QUECHUA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("RHAETO_ROMANCE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ROMANIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("RUNDI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("RUSSIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SAMOAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SANGO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SANSKRIT"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SCOTS"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SCOTS_GAELIC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SERBIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SESELWA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SESOTHO"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SHONA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SINDHI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SINHALESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SISWANT"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SLOVAK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SLOVENIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SOMALI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SPANISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SUNDANESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SWAHILI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SWEDISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("SYRIAC"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TAGALOG"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TAJIK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TAMIL"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TATAR"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TELUGU"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("THAI"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TIBETAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TIGRINYA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TONGA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TSONGA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TSWANA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TURKISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("TURKMEN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("UIGHUR"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("UKRAINIAN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("URDU"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("UZBEK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("VENDA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("VIETNAMESE"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("VOLAPUK"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("WARAY_PHILIPPINES"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("WELSH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("WOLOF"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("XHOSA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("X_Buginese"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("X_Gothic"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("X_KLINGON"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("X_PIG_LATIN"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("YIDDISH"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("YORUBA"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ZHUANG"));
  PyTuple_SET_ITEM(detLangs, upto++, PyUnicode_FromString("ZULU"));

  // Steals ref:
  PyModule_AddObject(m, "DETECTED_LANGUAGES", detLangs);

  if (upto != PyTuple_Size(detLangs)) {
    PyErr_SetString(st->error, "failed to initialize cld.DETECTED_LANGUAGES");
    INITERROR;
  }

  // Steals ref:
  PyModule_AddObject(m, "error", st->error);
#ifdef IS_PY3K
  return m;
#endif
}
