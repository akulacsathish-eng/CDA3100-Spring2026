#!/usr/bin/env python3
"""
Instructor script for Part 1 of the Memory Vault System.

This script reproduces the deterministic behaviour of the C reference
implementation for Part 1.  Given a student identifier, it computes
the pseudo‑random seed, generates the vault of uppercase letters,
builds the metadata nodes (including proper displacement offsets
reflecting the C `Node` structure layout), and then recovers the
password using pointer arithmetic semantics.  The recovered password
should match the output of the student program when `recover_password`
is implemented correctly.

Usage examples:

    python generate_answer.py U0000015860
    python generate_answer.py --json U0000015860

The script can emit plain text or JSON output.  If the `--json`
option is provided, the result is printed as a JSON object.  When
omitted, the script prints a human‑readable summary.

This script focuses on Part 1 only.  For Part 2, see the full
instructor generator in the project root.
"""

import argparse
import json
import ctypes
from typing import List, Dict, Any, Tuple


def compute_seed(student_id: str) -> int:
    """Extract digits from a student identifier and compute a 32‑bit seed."""
    digits = ''.join(ch for ch in student_id if ch.isdigit())
    if not digits:
        return 0
    id_num = int(digits)
    return (id_num * 1664525 + 1013904223) & 0x7FFFFFFF


def lcg_next(state: int) -> Tuple[int, int]:
    """Linear congruential generator: update and return new state and value."""
    next_state = (state * 1664525 + 1013904223) & 0x7FFFFFFF
    return next_state, next_state


def generate_vault(state: int) -> Tuple[List[List[str]], int]:
    """Generate an 8×12 vault of uppercase letters and return updated state."""
    vault: List[List[str]] = [[None for _ in range(12)] for _ in range(8)]
    for i in range(8):
        for j in range(12):
            state, r = lcg_next(state)
            vault[i][j] = chr(ord('A') + (r % 26))
    return vault, state


class NodeStruct(ctypes.Structure):
    """Replicate the C `Node` struct layout to compute offsets."""
    _fields_ = [
        ('valid', ctypes.c_char),        # 1 byte
        ('contributes', ctypes.c_char),  # 1 byte
        ('position', ctypes.c_ubyte),    # 1 byte
        ('row_index', ctypes.c_int),     # 4 bytes (alignment to 4)
        ('col_disp', ctypes.c_ubyte),    # 1 byte
        ('noise', ctypes.c_long),        # 8 bytes (alignment to 8)
        ('col_val', ctypes.c_ubyte),     # 1 byte
    ]


def col_offset() -> int:
    """Return the byte offset of the `col_val` field within the C Node."""
    # Accessing the `offset` attribute on the field descriptor yields its
    # offset in bytes relative to the start of the struct.  ctypes does
    # not expose offsetof directly, but each field has an `.offset`.
    return NodeStruct.col_val.offset  # type: ignore[attr-defined]


class Node:
    """Python representation of a metadata node."""
    def __init__(self,
                 position: int,
                 row_index: int,
                 col_val: int,
                 col_disp: int,
                 valid: int,
                 contributes: int,
                 noise: int) -> None:
        self.position = position
        self.row_index = row_index
        self.col_val = col_val
        self.col_disp = col_disp
        self.valid = valid
        self.contributes = contributes
        self.noise = noise


def generate_nodes(state: int) -> Tuple[List[Node], int, int]:
    """Generate a list of nodes and return updated state."""
    # Choose password length between 6 and 10
    state, r = lcg_next(state)
    length = 6 + (r % 5)
    nodes: List[Node] = []
    offset = col_offset()
    for i in range(length):
        valid = 1
        contributes = 1
        position = i
        # random row
        state, r_row = lcg_next(state)
        row_index = r_row % 8
        # random col
        state, r_col = lcg_next(state)
        col_val = r_col % 12
        # random 64‑bit noise
        state, low = lcg_next(state)
        state, high = lcg_next(state)
        noise = (high << 32) | low
        nodes.append(Node(position, row_index, col_val, offset, valid, contributes, noise))
    return nodes, length, state


def recover_password(nodes: List[Node], vault: List[List[str]]) -> str:
    """Recover the password by iterating nodes and using pointer semantics."""
    # Determine output length from maximum position among contributing nodes
    length = max((n.position for n in nodes if n.valid and n.contributes), default=-1) + 1
    out = ['?'] * length
    for n in nodes:
        if not n.valid or not n.contributes:
            continue
        row = n.row_index
        # Use pointer arithmetic concept: in C, col = *(base + col_disp).
        # Here, col_val holds the same value as dereferencing base+offset.
        col = n.col_val
        pos = n.position
        if 0 <= row < 8 and 0 <= col < 12 and 0 <= pos < length:
            out[pos] = vault[row][col]
    return ''.join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate expected password for Part 1')
    parser.add_argument('student_id', help='Student identifier (e.g., U0000015860)')
    parser.add_argument('--json', action='store_true', help='Output result as JSON')
    args = parser.parse_args()

    sid = args.student_id
    seed = compute_seed(sid)
    state = seed
    # Generate the vault and update state
    vault, state = generate_vault(state)
    # Generate nodes and update state
    nodes, length, state = generate_nodes(state)
    # Recover password
    password = recover_password(nodes, vault)

    if args.json:
        result: Dict[str, Any] = {
            'student_id': sid,
            'seed': seed,
            'part1': {
                'password': password,
            }
        }
        print(json.dumps(result, indent=2))
    else:
        print(f'Student ID: {sid}')
        print(f'Seed: {seed}')
        print('Part 1:')
        print(f'Password: {password}')


if __name__ == '__main__':
    main()