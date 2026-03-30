# Memory Vault System

This repository contains the complete implementation of the **Memory Vault System**, a four‑week final project designed for a junior‑level course in computer architecture.  The project blends low‑level C programming with assembly‑language control logic to reinforce concepts such as struct layout, memory alignment, pointer arithmetic, and conditional branching.  Students write portable C code for the first part of the assignment and Y86 assembly code for the second.

## Overview

The assignment is divided into two interconnected parts:

1. **Part 1 — Memory Vault (C + Memory Layout).**  Students analyse the layout of a custom metadata structure and apply pointer arithmetic to traverse a two‑dimensional “vault” of characters.  They must recover a hidden password by following metadata records and computing displacement offsets rather than using fixed field names.

2. **Part 2 — Vault Control Program (Y86 Assembly).**  Students write a non‑trivial program in Y86 assembly (a pedagogical subset of the x86‑64 instruction set).  The program iterates over an array of integers, computes a code based on even and odd index positions, compares it against a target value, and branches to an open or locked state.

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
├── part2/                 # Source files for Part 2
│   ├── README_part2.md
│   ├── y86_sim.py         # Y86 interpreter
│   └── program_template.y86
├── instructor/            # Scripts for instructors
│   ├── README_instructor.md
│   └── generate_answer.py # Generates expected answers for each student
└── pdf/                   # Instructional handouts and timeline 
    ├── Project_Timeline.pdf
    ├── Part1_Handout.pdf
    └── Part2_Handout.pdf
```

The **`part1`** directory contains a complete C project that can be compiled with GNU Make.  Students are expected to fill in the `recover_password` function in `main.c`.  All other functionality, including vault construction and metadata generation, is provided.  The **`part2`** directory offers a Python‑based interpreter for a small subset of the Y86 instruction set along with a starter assembly file.  Students write assembly code in that file, making use of loops, conditional jumps, and memory operations to compute the unlocking code.

 

Finally, the **`pdf`** directory (generated programmatically) holds handouts and a project timeline.  These documents explain the assignment in prose, outline the learning objectives, and provide a weekly timeline for completion.

## Building and Running

To build the C portion of the project, navigate to the `part1` directory and run:

```
make
```

This will produce an executable named `vault`.  Running the program requires a student identifier as input, either as a command‑line argument or interactively when prompted.  The program sets up the vault, generates metadata nodes based on the seed, and calls the yet‑to‑be‑implemented `recover_password` function.  Once implemented by the student, this function should populate a character buffer with the recovered password.

To work on Part 2, students should read `part2/README_part2.md`, complete `program_template.y86`, and use the provided `y86_sim.py` to execute their assembly program.  The simulator prints a summary of the computed code, the target code, and whether the vault opens.

