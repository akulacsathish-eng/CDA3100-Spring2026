#ifndef SEED_UTIL_H
#define SEED_UTIL_H

#include <stdint.h>

/*
 * Compute a deterministic seed from the student identifier.  The identifier
 * string is expected to contain an initial alphabetic prefix followed by
 * numeric characters (e.g., "U0000015860").  Only the numeric portion
 * is used in the computation.  The seed is derived via
 *   seed = (id_number * 1664525 + 1013904223) mod 2^31
 * which mirrors a common linear congruential generator.
 */
unsigned int compute_seed(const char *student_id);

/*
 * Produce the next pseudo-random value from the given state.  The state
 * is updated in place according to the same linear congruential formula
 * used in compute_seed().  The return value is the new state value.
 */
unsigned int lcg_next(unsigned int *state);

#endif /* SEED_UTIL_H */
