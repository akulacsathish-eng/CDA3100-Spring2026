#!/usr/bin/env python3
"""
Instructor script to generate expected outputs for the Memory Vault System.
This version matches the C execution flow exactly.
"""

import argparse
import json
from typing import List, Dict, Any, Tuple


def compute_seed(student_id: str) -> int:
    digits = ''.join(ch for ch in student_id if ch.isdigit())
    if not digits:
        return 0
    id_num = int(digits)
    seed = (id_num * 1664525 + 1013904223) & 0x7FFFFFFF
    return seed


def lcg_next(state: int) -> Tuple[int, int]:
    next_state = (state * 1664525 + 1013904223) & 0x7FFFFFFF
    return next_state, next_state


def generate_vault_and_state(state: int) -> Tuple[List[List[str]], int]:
    vault: List[List[str]] = [[None for _ in range(12)] for _ in range(8)]
    for i in range(8):
        for j in range(12):
            state, r = lcg_next(state)
            vault[i][j] = chr(ord('A') + (r % 26))
    return vault, state


class Node:
    def __init__(
        self,
        position: int,
        row_index: int,
        col_val: int,
        col_disp: int,
        valid: int,
        contributes: int,
        noise: int
    ) -> None:
        self.position = position
        self.row_index = row_index
        self.col_val = col_val
        self.col_disp = col_disp
        self.valid = valid
        self.contributes = contributes
        self.noise = noise


def generate_nodes_and_state(state: int) -> Tuple[List[Node], int, int]:
    state, r = lcg_next(state)
    length = 6 + (r % 5)

    nodes: List[Node] = []
    for i in range(length):
        valid = 1
        contributes = 1
        position = i

        state, r_row = lcg_next(state)
        row_index = r_row % 8

        state, r_col = lcg_next(state)
        col_val = r_col % 12

        col_disp = 0  # not used in this simplified instructor version

        state, low = lcg_next(state)
        state, high = lcg_next(state)
        noise = (high << 32) | low

        nodes.append(Node(position, row_index, col_val, col_disp, valid, contributes, noise))

    return nodes, length, state


def recover_password(nodes: List[Node], vault: List[List[str]]) -> str:
    length = max((n.position for n in nodes if n.valid and n.contributes), default=-1) + 1
    out = ['?'] * length
    for n in nodes:
        if not n.valid or not n.contributes:
            continue
        row = n.row_index
        col = n.col_val
        pos = n.position
        out[pos] = vault[row][col]
    return ''.join(out)


def generate_array_and_target(seed: int) -> Tuple[List[int], int, int]:
    state = seed
    state, rv = lcg_next(state)
    length = 4 + (rv % 5)

    arr: List[int] = []
    for _ in range(length):
        state, rv = lcg_next(state)
        arr.append((rv % 9) + 1)

    code = 0
    for i, val in enumerate(arr):
        code += val if (i % 2 == 0) else -val

    target = code
    return arr, code, target


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate expected outputs for the Memory Vault System")
    parser.add_argument("student_id", help="Student identifier (e.g., U0000015860)")
    parser.add_argument("--part1", action="store_true", help="Output only Part 1 result")
    parser.add_argument("--part2", action="store_true", help="Output only Part 2 result")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    parser.add_argument("--output", type=str, help="Write output to the specified file")
    args = parser.parse_args()

    sid = args.student_id
    seed = compute_seed(sid)

    # Match C flow exactly:
    # state starts at seed
    # generate_vault updates state
    # generate_nodes uses the updated state
    state = seed
    vault, state = generate_vault_and_state(state)
    nodes, length, state = generate_nodes_and_state(state)
    password = recover_password(nodes, vault)

    arr, code, target = generate_array_and_target(seed)
    expected_result = "VAULT OPEN" if code == target else "VAULT LOCKED"

    show_p1 = not args.part2 or args.part1
    show_p2 = not args.part1 or args.part2

    if args.json:
        data: Dict[str, Any] = {
            "student_id": sid,
            "seed": seed,
        }
        if show_p1:
            data["part1"] = {
                "password": password,
            }
        if show_p2:
            data["part2"] = {
                "array": arr,
                "target": target,
                "expected_result": expected_result,
            }
        text = json.dumps(data, indent=2)
    else:
        lines: List[str] = []
        lines.append(f"Student ID: {sid}")
        lines.append(f"Seed: {seed}\n")
        if show_p1:
            lines.append("Part 1:")
            lines.append(f"Password: {password}\n")
        if show_p2:
            lines.append("Part 2:")
            lines.append(f"Array: {arr}")
            lines.append(f"Target: {target}")
            lines.append(f"Expected Result: {expected_result}")
        text = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)


if __name__ == "__main__":
    main()