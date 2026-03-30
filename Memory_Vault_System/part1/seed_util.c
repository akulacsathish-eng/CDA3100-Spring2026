#include "seed_util.h"

#include <ctype.h>

/*
 * Extracts the numeric component of the student identifier and use
 */
unsigned int compute_seed(const char *student_id) {
    unsigned long id_num = 0;
    if (student_id == NULL) {
        return 0;
    }
    while (*student_id) {
        if (isdigit((unsigned char)*student_id)) {
            id_num = id_num * 10 + (unsigned long)(*student_id - '0');
        }
        student_id++;
    }
    /* Perform the seed computation in 64‑bit space to avoid overflow */
    unsigned long long product = (unsigned long long)id_num * 1664525ULL;
    unsigned long long sum = product + 1013904223ULL;
    unsigned long long mod = sum & 0x7fffffffULL; /* modulo 2^31 */
    return (unsigned int)mod;
}

/*
 * Update the pseudo‑random state using the same LCG formula as in
 * compute_seed.  Modulo 2^31 ensures the result fits into 31 bits.
 */
unsigned int lcg_next(unsigned int *state) {
    if (state == NULL) {
        return 0;
    }
    unsigned long long next = (unsigned long long)(*state) * 1664525ULL + 1013904223ULL;
    next &= 0x7fffffffULL;
    *state = (unsigned int)next;
    return *state;
}
