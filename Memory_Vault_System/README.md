# Memory Vault System


The assignment is divided into two interconnected parts:

1. **Part 1 — Memory Vault (C + Memory Layout).**  Students analyse the layout of a custom metadata structure and apply pointer arithmetic to traverse a two‑dimensional “vault” of characters.  They must recover a hidden password by following metadata records and computing displacement offsets rather than using fixed field names.

2. **Part 2 — Vault Control Program (Y86 Assembly).**  TBD

The system is **deterministic**.  Personalisation is achieved via a seed computed from each student’s numeric identifier.  No per‑student source files exist; all variation occurs at runtime through the seed.

## Repository Structure

```
memory_vault_system/
├── README.md              # General overview (this file)
├── part1/                 # Source and build files for Part 1
│   ├── Makefile
│   ├── README_part1.md
│   ├── main.c
│   ├── vault_gen.c
│   ├── vault_gen.h
│   ├── seed_util.c
│   ├── seed_util.h
│   └── (student implements recover_password in main.c)

├── instructor/ 
│   └── generate_answer.py # Generates expected answers for each student
└── pdf/                   # Instructional handouts and timeline 
    ├── Project_Timeline.pdf
    ├── Part1_Handout.pdf
    └── Part2_Handout.pdf
```

The **`part1`** directory contains a complete C project that can be compiled with GNU Make.  Students are expected to fill in the `recover_password` function in `main.c`.  All other functionality, including vault construction and metadata generation, is provided.  

 

Finally, the **`pdf`** directory (generated programmatically) holds handouts and a project timeline.  These documents explain the assignment in prose, outline the learning objectives, and provide a weekly timeline for completion.

## Building and Running

To build the C portion of the project, navigate to the `part1` directory and run:

```
make
```

This will produce an executable named `vault`.  Running the program requires a student identifier as input, either as a command‑line argument or interactively when prompted.  The program sets up the vault, generates metadata nodes based on the seed, and calls the yet‑to‑be‑implemented `recover_password` function.  Once implemented by the student, this function should populate a character buffer with the recovered password.

. Review your answer by running the script ./python generate_answer.py studentID

