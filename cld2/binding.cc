#include <cstdlib>
#include <cstdio>

#include "compact_lang_det.h"
#include "encodings.h"
#include "generated_language.h"
#include "binding.h"

// Fwd declaration from encoding_lut.cc
CLD2::Encoding EncodingFromName(const char *name);
extern const char* const cld_encodings[];

// Fwd declaration from generated_language.cc
namespace CLD2 {
    extern const char* const kLanguageToName[];
    extern const int kLanguageToNameSize;
    extern const int kLanguageToCodeSize;
    extern const char* const kLanguageToCode[];
}

extern "C" {

    int cld_num_languages() {
        return CLD2::kLanguageToNameSize;
    }

    const char** cld_languages() {
        return (const char**) &CLD2::kLanguageToName;
    }

    int cld_num_langcodes() {
        return CLD2::kLanguageToCodeSize;
    } 

    const char** cld_langcodes() {
        return (const char**) &CLD2::kLanguageToCode;
    }

    int cld_num_encodings() {
        return CLD2::NUM_ENCODINGS;
    }

    const char** cld_supported_encodings() {
        return (const char**) &cld_encodings;
    }

    cld_results_t *cld_create_results() {
        cld_results_t *res = (cld_results_t*) calloc(1, sizeof(cld_results_t));
        if (res == NULL)
            return NULL;

        res->results = (cld_result_t*) calloc(3, sizeof(cld_result_t));

        if (res->results == NULL) {
            free(res);
            return NULL;
        }

        return res;
    }

    void cld_destroy_results(cld_results_t *results) {
        if (results->chunks != NULL) {
            free(results->chunks);
        }
        free(results->results);
        free(results);
    }

    int cld_detect(char *bytes, int num_bytes, 
            cld_results_t *results,
            const char *hint_content_language,
            const char *hint_tld, 
            const char *hint_language, 
            const char *hint_encoding,
            int is_plain_text,
            int return_vectors,
            int best_effort,
            int debug_score_as_quads,
            int debug_html,
            int debug_cr,
            int debug_verbose,
            int debug_quiet,
            int debug_echo) {

        CLD2::CLDHints cldHints;
        cldHints.tld_hint = 0;
        cldHints.content_language_hint = 0;

        int flags = 0;
        if (debug_score_as_quads != 0)
            flags |= CLD2::kCLDFlagScoreAsQuads;
        if (debug_html != 0)
            flags |= CLD2::kCLDFlagHtml;
        if (debug_cr != 0)
            flags |= CLD2::kCLDFlagCr;
        if (debug_verbose != 0)
            flags |= CLD2::kCLDFlagVerbose;
        if (debug_quiet != 0)
            flags |= CLD2::kCLDFlagQuiet;
        if (debug_echo != 0)
            flags |= CLD2::kCLDFlagEcho;
        if (best_effort != 0)
            flags |= CLD2::kCLDFlagBestEffort;

        if (hint_language == NULL) {
            cldHints.language_hint = CLD2::UNKNOWN_LANGUAGE;
        } else {
            cldHints.language_hint = CLD2::GetLanguageFromName(hint_language);
            if (cldHints.language_hint == CLD2::UNKNOWN_LANGUAGE)
                return 1;
        }

        if (hint_encoding == 0) {
            cldHints.encoding_hint = CLD2::UNKNOWN_ENCODING;
        } else {
            cldHints.encoding_hint = EncodingFromName(hint_encoding);
            if (cldHints.encoding_hint == CLD2::UNKNOWN_ENCODING)
                return 2;
        }

        bool is_reliable;
        CLD2::Language language3[3];
        int percent3[3];
        double normalized_score3[3];
        int text_bytes_found;
        int valid_prefix_bytes;
        CLD2::ResultChunkVector resultChunkVector;

        CLD2::ExtDetectLanguageSummaryCheckUTF8(bytes, num_bytes,
                                                is_plain_text != 0,
                                                &cldHints,
                                                flags,
                                                language3,
                                                percent3,
                                                normalized_score3,
                                                return_vectors != 0 ? &resultChunkVector : 0,
                                                &text_bytes_found,
                                                &is_reliable,
                                                &valid_prefix_bytes);

        results->reliable = is_reliable;
        results->bytes_found = text_bytes_found;
        results->valid_prefix_bytes = valid_prefix_bytes;

        if (valid_prefix_bytes < num_bytes)
            return 3;

        for(int idx=0; idx<3; idx++) {
            CLD2::Language lang = language3[idx];
            cld_result_t *result = &(results->results[idx]);
            result->lang_name = CLD2::LanguageName(lang);
            result->lang_code = CLD2::LanguageCode(lang);
            result->percent = percent3[idx];
            result->normalized_score = normalized_score3[idx];
        }

        if (return_vectors != 0) {
            int num_chunks = resultChunkVector.size();
            results->chunks = (cld_chunk_t*) calloc(num_chunks, sizeof(cld_chunk_t));
            // Dont care if we failed the calloc, we can return a NULL to the PySide, it
            // will check for that and return no chunks
            if (results->chunks != NULL) {
                results->num_chunks = num_chunks;
                for (unsigned int i=0; i<num_chunks; i++) {
                    CLD2::ResultChunk chunk = resultChunkVector.at(i);
                    CLD2::Language lang = static_cast<CLD2::Language>(chunk.lang1);
                    cld_chunk_t *res_chunk = &(results->chunks[i]);
                    res_chunk->offset = chunk.offset;
                    res_chunk->bytes = chunk.bytes;
                    res_chunk->lang_name = CLD2::LanguageName(lang);
                    res_chunk->lang_code = CLD2::LanguageCode(lang);
                }
            }
        }

        return 0;
    }
}
