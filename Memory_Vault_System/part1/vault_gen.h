#ifndef VAULT_GEN_H
#define VAULT_GEN_H

#include <stddef.h>

/*
 * Part 1 defines a metadata structure used to describe how to extract
 * characters from a two–dimensional vault. 
 */
typedef struct {
    char valid;           /* non‑zero when this node is considered */
    char contributes;     /* non‑zero when this node contributes a character */
    unsigned char position; /* index into the output password */
    int row_index;        /* index of the row in the vault */
    unsigned char col_disp; /* byte offset of the column value within this struct */
    long noise;           /* unused padding/noise field */
    unsigned char col_val; /* stores the actual column index */
} Node;

/* Dimensions of the vault */
#define ROWS 8
#define COLS 12

/*
 * Fills the vault with deterministic uppercase letters based on the
 * provided pseudo‑random state.  
 */
void generate_vault(char vault[ROWS][COLS], unsigned int *state);

/*
 * Allocates and fills an array of Node structures.  The length of the
 * array is stored in *out_len.  
 */
Node *generate_nodes(int *out_len, unsigned int *state);

#endif /* VAULT_GEN_H */
