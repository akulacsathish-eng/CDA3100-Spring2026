#include "vault_gen.h"
#include "seed_util.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Placeholder implementation of recover_password.  Students should
 * replace the body of this function with an implementation that
 * traverses the metadata records, applies pointer arithmetic to
 * compute column indices, and populates the output buffer.  See
 * README_part1.md for details.
 */
void recover_password(Node *nodes, char vault[][COLS], int len, char *out) {
    if (nodes == NULL || out == NULL) {
        return;
    }

    /*
     * TODO:
     * Implement password recovery.
     *
     * Requirements:
     * 1. Iterate through all nodes.
     * 2. Ignore nodes that are not valid or do not contribute.
     * 3. Compute the column index using pointer arithmetic and col_disp.
     * 4. Use row_index and the computed column to read from vault[row][col].
     * 5. Store the recovered character into out[position].
     * 6. Null-terminate the output string.
     */

    for (int i = 0; i < len; i++) {
        out[i] = '?';
    }
    out[len] = '\0';
}

int main(int argc, char *argv[]) {
    char student_id[64] = {0};
    if (argc >= 2) {
        /* Copy at most 63 characters to avoid overflow */
        strncpy(student_id, argv[1], sizeof(student_id) - 1);
    } else {
        printf("Enter student ID: ");
        if (scanf("%63s", student_id) != 1) {
            fprintf(stderr, "Failed to read student ID\n");
            return 1;
        }
    }

    /* Compute the deterministic seed and initialise the pseudo-random state */
    unsigned int seed = compute_seed(student_id);
    unsigned int state = seed;

    /* Generate the vault of characters */
    char vault[ROWS][COLS];
    generate_vault(vault, &state);

    /* Generate the metadata nodes */
    int len = 0;
    Node *nodes = generate_nodes(&len, &state);
    if (nodes == NULL) {
        fprintf(stderr, "Failed to allocate nodes\n");
        return 1;
    }

    /* Allocate buffer for the recovered password */
    char *password = (char *)malloc((size_t)len + 1);
    if (password == NULL) {
        free(nodes);
        fprintf(stderr, "Memory allocation failure\n");
        return 1;
    }

    /* Recover the password via pointer arithmetic (student implements) */
    recover_password(nodes, vault, len, password);

    printf("Password recovered: %s\n", password);

    /* Clean up */
    free(password);
    free(nodes);

    return 0;
}
