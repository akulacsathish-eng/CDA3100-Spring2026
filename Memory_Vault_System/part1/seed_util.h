#ifndef SEED_UTIL_H
#define SEED_UTIL_H

#include <stdint.h>

/*
 * Compute a deterministic seed from the student identifier.  

 */
unsigned int compute_seed(const char *student_id);

/*
 * Produce the next pseudo‑random value from the given state.  
 */
unsigned int lcg_next(unsigned int *state);

#endif /* SEED_UTIL_H */
