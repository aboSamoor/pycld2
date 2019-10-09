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

#include <stdio.h>
#include <string.h>  // Windows compat (vs. strings.h)
#include <ctype.h>

#include "compact_lang_det.h"
#include "encodings.h"

struct cld_encoding {
  const char *name;
  CLD2::Encoding encoding;
};

extern const cld_encoding cld_encoding_info[] = {
  {"ISO_8859_1", CLD2::ISO_8859_1},
  {"ISO_8859_2", CLD2::ISO_8859_2},
  {"ISO_8859_3", CLD2::ISO_8859_3},
  {"ISO_8859_4", CLD2::ISO_8859_4},
  {"ISO_8859_5", CLD2::ISO_8859_5},
  {"ISO_8859_6", CLD2::ISO_8859_6},
  {"ISO_8859_7", CLD2::ISO_8859_7},
  {"ISO_8859_8", CLD2::ISO_8859_8},
  {"ISO_8859_9", CLD2::ISO_8859_9},
  {"ISO_8859_10", CLD2::ISO_8859_10},
  {"JAPANESE_EUC_JP", CLD2::JAPANESE_EUC_JP},
  {"JAPANESE_SHIFT_JIS", CLD2::JAPANESE_SHIFT_JIS},
  {"JAPANESE_JIS", CLD2::JAPANESE_JIS},
  {"CHINESE_BIG5", CLD2::CHINESE_BIG5},
  {"CHINESE_GB", CLD2::CHINESE_GB},
  {"CHINESE_EUC_CN", CLD2::CHINESE_EUC_CN},
  {"KOREAN_EUC_KR", CLD2::KOREAN_EUC_KR},
  {"UNICODE_UNUSED", CLD2::UNICODE_UNUSED},
  {"CHINESE_EUC_DEC", CLD2::CHINESE_EUC_DEC},
  {"CHINESE_CNS", CLD2::CHINESE_CNS},
  {"CHINESE_BIG5_CP950", CLD2::CHINESE_BIG5_CP950},
  {"JAPANESE_CP932", CLD2::JAPANESE_CP932},
  {"UTF8", CLD2::UTF8},
  {"UNKNOWN_ENCODING", CLD2::UNKNOWN_ENCODING},
  {"ASCII_7BIT", CLD2::ASCII_7BIT},
  {"RUSSIAN_KOI8_R", CLD2::RUSSIAN_KOI8_R},
  {"RUSSIAN_CP1251", CLD2::RUSSIAN_CP1251},
  {"MSFT_CP1252", CLD2::MSFT_CP1252},
  {"RUSSIAN_KOI8_RU", CLD2::RUSSIAN_KOI8_RU},
  {"MSFT_CP1250", CLD2::MSFT_CP1250},
  {"ISO_8859_15", CLD2::ISO_8859_15},
  {"MSFT_CP1254", CLD2::MSFT_CP1254},
  {"MSFT_CP1257", CLD2::MSFT_CP1257},
  {"ISO_8859_11", CLD2::ISO_8859_11},
  {"MSFT_CP874", CLD2::MSFT_CP874},
  {"MSFT_CP1256", CLD2::MSFT_CP1256},
  {"MSFT_CP1255", CLD2::MSFT_CP1255},
  {"ISO_8859_8_I", CLD2::ISO_8859_8_I},
  {"HEBREW_VISUAL", CLD2::HEBREW_VISUAL},
  {"CZECH_CP852", CLD2::CZECH_CP852},
  {"CZECH_CSN_369103", CLD2::CZECH_CSN_369103},
  {"MSFT_CP1253", CLD2::MSFT_CP1253},
  {"RUSSIAN_CP866", CLD2::RUSSIAN_CP866},
  {"ISO_8859_13", CLD2::ISO_8859_13},
  {"ISO_2022_KR", CLD2::ISO_2022_KR},
  {"GBK", CLD2::GBK},
  {"GB18030", CLD2::GB18030},
  {"BIG5_HKSCS", CLD2::BIG5_HKSCS},
  {"ISO_2022_CN", CLD2::ISO_2022_CN},
  {"TSCII", CLD2::TSCII},
  {"TAMIL_MONO", CLD2::TAMIL_MONO},
  {"TAMIL_BI", CLD2::TAMIL_BI},
  {"JAGRAN", CLD2::JAGRAN},
  {"MACINTOSH_ROMAN", CLD2::MACINTOSH_ROMAN},
  {"UTF7", CLD2::UTF7},
  {"BHASKAR", CLD2::BHASKAR},
  {"HTCHANAKYA", CLD2::HTCHANAKYA},
  {"UTF16BE", CLD2::UTF16BE},
  {"UTF16LE", CLD2::UTF16LE},
  {"UTF32BE", CLD2::UTF32BE},
  {"UTF32LE", CLD2::UTF32LE},
  {"BINARYENC", CLD2::BINARYENC},
  {"HZ_GB_2312", CLD2::HZ_GB_2312},
  {"UTF8UTF8", CLD2::UTF8UTF8},
  {"TAM_ELANGO", CLD2::TAM_ELANGO},
  {"TAM_LTTMBARANI", CLD2::TAM_LTTMBARANI},
  {"TAM_SHREE", CLD2::TAM_SHREE},
  {"TAM_TBOOMIS", CLD2::TAM_TBOOMIS},
  {"TAM_TMNEWS", CLD2::TAM_TMNEWS},
  {"TAM_WEBTAMIL", CLD2::TAM_WEBTAMIL},
  {"KDDI_SHIFT_JIS", CLD2::KDDI_SHIFT_JIS},
  {"DOCOMO_SHIFT_JIS", CLD2::DOCOMO_SHIFT_JIS},
  {"SOFTBANK_SHIFT_JIS", CLD2::SOFTBANK_SHIFT_JIS},
  {"KDDI_ISO_2022_JP", CLD2::KDDI_ISO_2022_JP},
  {"SOFTBANK_ISO_2022_JP", CLD2::SOFTBANK_ISO_2022_JP},
};

// Re-written (simplified) from BSD strings.h
inline int
strcasecmp(const char *s1, const char *s2)
{
  for (;;) {
    int c1 = tolower(*((unsigned char *) s1++));
    int c2 = tolower(*((unsigned char *) s2++));
    if ((c1 != c2) || (c1 == '\0')) {
      return c1 - c2;
    }
  }
  return 0;
}

CLD2::Encoding EncodingFromName(const char *name) {
  for (int i = 0; i < CLD2::NUM_ENCODINGS; i++) {
    if (!strcasecmp(cld_encoding_info[i].name, name)) {
      return cld_encoding_info[i].encoding;
    }
  }

  return CLD2::UNKNOWN_ENCODING;
}
