# CDA 3100 — Chapter 4: Machine Basics (C → Assembly)

These programs are designed to support in-class explanation of how C code
maps to machine-level behavior and x86-64 assembly instructions.

Each file focuses on one major concept from Chapter 4.

------------------------------------------------------------

## File List and Purpose

### 01_bytes_endianness.c
Shows that data is stored as raw bytes in memory.
Useful for explaining:
- Byte-level representation
- Endianness
- Memory addresses

Compile:
gcc -Og 01_bytes_endianness.c -o bytes

------------------------------------------------------------

### 02_function_call_and_return.c
Demonstrates:
- Function calls
- Return values
- Storing results through pointers

Useful to inspect:
- call instruction
- return value in %rax
- movq into memory

Compile:
gcc -Og 02_function_call_and_return.c -o call

------------------------------------------------------------

### 03_pointer_swap.c
Classic pointer-based swap example.

Demonstrates:
- Dereferencing pointers
- Memory loads and stores
- Passing addresses to functions

Compile:
gcc -Og 03_pointer_swap.c -o swap

------------------------------------------------------------

### 04_addressing_modes_array.c
Uses array indexing with stride.

Demonstrates:
- Base + index × scale addressing
- How arrays map to memory references

Typical addressing form in assembly:
D(Rb, Ri, S)

Compile:
gcc -Og 04_addressing_modes_array.c -o addr

------------------------------------------------------------

### 05_leaq_and_arithmetic.c
Shows arithmetic that is often implemented using:
- leaq
- shifts and adds

Demonstrates:
- leaq used for computation (not just addresses)
- Mixed arithmetic instruction sequences

Compile:
gcc -Og 05_leaq_and_arithmetic.c -o arith

------------------------------------------------------------

### 06_shift_operations.c
Shows difference between:
- Arithmetic right shift (signed)
- Logical right shift (unsigned)
- Left shift

Maps to:
- sar
- shr
- sal/shl

Compile:
gcc -Og 06_shift_operations.c -o shift

------------------------------------------------------------

## Viewing Assembly

To see generated assembly:

gcc -Og -S filename.c

To see object code disassembly:

gcc -Og -c filename.c


objdump -d filename.o

To disassemble executable:

objdump -d program_name

------------------------------------------------------------

Note:
-Og keeps code readable while still applying basic optimizations.

