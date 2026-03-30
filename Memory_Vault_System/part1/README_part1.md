# Part 1: Memory Vault (C)

In this part of the Memory Vault System you will work entirely in the C programming language.  You are given a two‑dimensional array of characters (the *vault*) and a sequence of metadata records (the *nodes*).  Each metadata record describes how to extract a single character from the vault and where to place that character in the final password string.

Your primary learning objectives in Part 1 are:

* **Struct layout and padding.**  Examine the provided `Node` structure.  Notice that it contains a mixture of `char`, `unsigned char`, `int`, and `long` fields.  Because of alignment requirements, the compiler inserts padding bytes between some fields.  Understanding where these gaps appear is critical for computing displacement offsets correctly.
* **Pointer arithmetic.**  You must compute the column index for a given node by taking a pointer to the structure, adding a displacement, and dereferencing the result.  Directly accessing the `col_val` field through the structure name is not permitted in the final implementation.
* **Traversal of metadata records.**  You will iterate over an array of nodes, test validity and contribution flags, and assemble the recovered password in an output buffer.  Some nodes may be marked as non‑contributing; these should be ignored.

The header `vault_gen.h` declares the `Node` structure and functions used to build the vault and generate the nodes.  The header `seed_util.h` declares a function that converts a student identifier into a deterministic seed and a linear congruential generator for pseudo‑random number generation.

## Implementation Tasks

1. **Compile the project.**  In the `part1` directory, run `make` to build the executable named `vault`.  This will compile the provided sources and link them together.

2. **Run the program.**  You can execute the compiled program by supplying a student identifier as a command‑line argument:

   ```
   ./vault U0000015860
   ```

   If no argument is supplied, the program will prompt for a student identifier.  The program allocates the vault and node array, then calls `recover_password` to produce the password.  Until you implement `recover_password` the program will output a placeholder string.

3. **Implement `recover_password`.**  Open `main.c` and locate the function:

   ```c
   void recover_password(Node *nodes, char vault[][COLS], int len, char *out);
   ```

   Replace the stub implementation with logic that iterates over the `len` nodes.  For each node whose `valid` and `contributes` fields are both non‑zero, compute the column index using pointer arithmetic rather than direct field access:

   ```c
   // base is a byte pointer to the start of the node
   unsigned char *base = (unsigned char *)&nodes[i];
   // add the displacement stored in col_disp to get a pointer to the column value
   unsigned char col = *(base + nodes[i].col_disp);
   ```

   Use the `row_index` and computed `col` values to select a character from the vault (`vault[row][col]`) and place it into the output buffer at position `position`.  Ensure that the output buffer is null‑terminated when done.

4. **Test your implementation.**  You can compare your recovered password against the instructor script (`instructor/generate_answer.py`) to verify correctness.  The instructor script uses the same seed logic and will display the correct password for a given student identifier.

## Notes

* Do not alter the provided `Node` structure or the functions in `vault_gen.c` and `seed_util.c`.  All personalisation is derived from the seed, and modifying these files may break reproducibility.
* The program uses dynamic memory allocation for the node array and password buffer; be sure to free any allocated memory to avoid leaks.
