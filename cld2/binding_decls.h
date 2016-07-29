// The bindings, this file is kept clean from None C syntax
// (e.g. the preprocessor) in order to allow both C and python
// to read this file.
typedef struct {
    const char *lang_name;
    const char *lang_code;
    int percent;
    double normalized_score;
} cld_result_t;

typedef struct {
    int offset;
    int bytes;
    const char *lang_name;
    const char *lang_code;
} cld_chunk_t;

typedef struct {
    cld_result_t *results;
    cld_chunk_t *chunks;
    int num_chunks;
    int reliable;
    int bytes_found;
    int valid_prefix_bytes;
} cld_results_t;

typedef struct {
    char *lang_name;
    char *lang_code;
} cld_language_details_t;

int cld_num_languages();
const char** cld_languages();
int cld_num_langcodes();
const char** cld_langcodes();
int cld_num_encodings();
const char** cld_supported_encodings();

cld_results_t* cld_create_results();

void cld_destroy_results(cld_results_t *results);

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
        int debug_echo);
