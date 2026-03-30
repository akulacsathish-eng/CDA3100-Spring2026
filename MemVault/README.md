# Memory Vault System

This repository contains the complete implementation of the **Memory Vault System**


The assignment is divided into two interconnected parts:

1. **Part 1 - Memory Vault (C + Memory Layout).** Students analyse the layout of a custom metadata structure and apply pointer arithmetic to traverse a two-dimensional "vault" of characters. They must recover a hidden password by following metadata records and computing displacement offsets rather than using fixed field names.
2. **Part 2 - Vault Control Program (Y86 Assembly).** 
TBD



## Repository Structure

```
memory _vault _system/
|-- README.md              # General overview (this file)
|-- part1/                 # Source and build files for Part 1
|   |-- Makefile
|   |-- README _part1.md
|   |-- main.c
|   |-- vault _gen.c
|   |-- vault _gen.h
|   |-- seed _util.c
|   |-- seed _util.h
|   `-- (student implements recover _password in main.c)
||-- instructor/            # Scripts for instructors
|   |-- README _instructor.md
|   `-- generate _answer.py # Generates expected answers for each student
`-- pdf/                   # Instructional handouts and timeline

The **part1** directory contains a complete C project that can be compiled with GNU Make. Students are expected to fill in the `recover _password` function in `main.c`. All other functionality, including vault construction and metadata generation, is provided.





The **part2** directory TBD.



The **instructor** folder contains a script that allows teaching staff to compute personalised expected outputs for any student identifier. The script uses the same seed logic as the student programs and therefore reproduces the password and code generation exactly. It also supports optional flags for partial output and JSON formatting.



Finally, the **pdf** directory (generated programmatically) holds handouts and a project timeline. These documents explain the assignment in prose, outline the learning objectives, and provide a weekly timeline for completion.

## Building and Running

To build the C portion of the project, navigate to the `part1` directory and run:

```
make
```

This will produce an executable named `vault`. Running the program requires a student identifier as input, either as a command-line argument or interactively when prompted. The program sets up the vault, generates metadata nodes based on the seed, and calls the yet-to-be-implemented `recover _password` function. Once implemented by the student, this function should populate a character buffer with the recovered password.



To work on Part 2, TBD



## 

