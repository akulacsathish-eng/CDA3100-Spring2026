#include "vault_gen.h"
#include "seed_util.h"

#include <stdlib.h>
#include <stddef.h>

/*
 * Fill the vault with deterministic uppercase letters using a linear
 * congruential generator.  Each call to lcg_next() updates the state
 * in place and returns a new pseudo‑random value.  The vault is
 * eight rows by twelve columns; values wrap into the range A–Z.
 */
void generate_vault(char vault[ROWS][COLS], unsigned int *state) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            unsigned int r = lcg_next(state);
            vault[i][j] = (char)('A' + (r % 26));
        }
    }
}

/*
 * Generate an array of Node structures.  The length is chosen in the
 * range [6, 10] for variety.  Each node will reference a random
 * location within the vault.  The displacement field is set to the
 * offset of the col_val field within the Node structure so that
 * students must compute the column index via pointer arithmetic.
 */
Node *generate_nodes(int *out_len, unsigned int *state) {
    if (out_len == NULL || state == NULL) {
        return NULL;
    }
    /* Choose a password length between 6 and 10 inclusive */
    int len = 6 + (int)(lcg_next(state) % 5); /* yields 6–10 */
    Node *nodes = (Node *)malloc((size_t)len * sizeof(Node));
    if (nodes == NULL) {
        *out_len = 0;
        return NULL;
    }
    for (int i = 0; i < len; i++) {
        nodes[i].valid = 1;
        nodes[i].contributes = 1;
        nodes[i].position = (unsigned char)i;
        /* Randomly choose a row in the vault */
        unsigned int r_row = lcg_next(state);
        nodes[i].row_index = (int)(r_row % ROWS);
        /* Randomly choose a column and store it in col_val */
        unsigned int r_col = lcg_next(state);
        nodes[i].col_val = (unsigned char)(r_col % COLS);
        /* Set displacement to the offset of col_val within the struct */
        nodes[i].col_disp = (unsigned char)offsetof(Node, col_val);
        /* Generate a 64‑bit noise value by combining two 32‑bit random numbers */
        unsigned long long low = (unsigned long long)lcg_next(state);
        unsigned long long high = (unsigned long long)lcg_next(state);
        nodes[i].noise = (long)((high << 32) | low);
    }
    *out_len = len;
    return nodes;
}
