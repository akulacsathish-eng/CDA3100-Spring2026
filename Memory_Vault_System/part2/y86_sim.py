#!/usr/bin/env python3
"""
Y86 Simulator for the Memory Vault System.

This interpreter executes a small subset of the Y86 instruction set and
provides deterministic personalisation based on a student identifier.  It
expects an assembly source file as its first argument.  An optional
second argument may specify a student ID; if omitted, the simulator
prompts for it.  The simulator then computes a seed from the ID,
generates an array of integer values, a target code, and initialises
registers and memory.  After execution, it prints a summary of the
final code, the target code, and whether the vault opens.

Supported instructions:
  irmovq $imm, %rA
  irmovq label, %rA
  rrmovq %rA, %rB
  addq %rA, %rB
  subq %rA, %rB
  andq %rA, %rB
  mrmovq D(%rA), %rB
  mrmovq D(%rA,%rB), %rC
  mrmovq (%rA,%rB), %rC
  jmp label
  je label
  jne label
  halt

Labels are defined by lines of the form `label:`.  Comments start with
`#` and are ignored.  Blank lines are skipped.  The zero flag (ZF) is
set when the result of an arithmetic operation is zero and cleared
otherwise.  Conditional jumps depend solely on ZF.

Example usage:
    python y86_sim.py program_template.y86 U0000015860

This will run the provided program for the student identifier
``U0000015860`` and display the summary.
"""
import sys
import re
from typing import List, Dict, Tuple, Union


def compute_seed(student_id: str) -> int:
    """Compute deterministic seed from numeric portion of ID."""
    digits = ''.join(ch for ch in student_id if ch.isdigit())
    if digits == '':
        return 0
    id_num = int(digits)
    # Use the same constants as in the C implementation
    seed64 = (id_num * 1664525 + 1013904223) & 0x7FFFFFFF
    return seed64


def lcg_next(state: int) -> Tuple[int, int]:
    """Linear congruential generator yielding next state and value."""
    next_state = (state * 1664525 + 1013904223) & 0x7FFFFFFF
    return next_state, next_state


def generate_array_and_result(seed: int) -> Tuple[List[int], int]:
    """Generate an array of integers and compute its result code.

    The result is the sum of values at even indices minus the sum of values at odd indices.
    """
    state = seed
    # Choose array length in range [4, 8]
    state, r = lcg_next(state)
    length = 4 + (r % 5)  # 4–8 inclusive
    array: List[int] = []
    for _ in range(length):
        state, rv = lcg_next(state)
        array.append((rv % 9) + 1)  # values 1–9
    # Compute result code: sum of even indices minus sum of odd indices
    result = 0
    for i, val in enumerate(array):
        if i % 2 == 0:
            result += val
        else:
            result -= val
    return array, result

# -----------------------------------------------------------------------------
# Password‑based vault integration
#
# To integrate Part 1 and Part 2, we compute the expected password from the
# student identifier and use it to determine the target code.  If the
# simulator is invoked with the correct password, the target code equals the
# computed result so the vault can open.  If the password is absent or
# incorrect, the target is offset by 1, causing the vault to remain locked.
#
# These helper functions replicate the password recovery logic from the Part 1
# implementation.  They intentionally mirror the instructor script to ensure
# that the student‑facing and instructor‑facing results agree.

class Node:
    def __init__(self, position: int, row_index: int, col_val: int, col_disp: int, valid: int, contributes: int, noise: int) -> None:
        self.position = position
        self.row_index = row_index
        self.col_val = col_val
        self.col_disp = col_disp
        self.valid = valid
        self.contributes = contributes
        self.noise = noise


def generate_vault(seed: int) -> List[List[str]]:
    """Generate the 8×12 vault of characters for password recovery."""
    state = seed
    vault: List[List[str]] = [[None for _ in range(12)] for _ in range(8)]
    for i in range(8):
        for j in range(12):
            state, r = lcg_next(state)
            vault[i][j] = chr(ord('A') + (r % 26))
    return vault


def generate_nodes(seed: int) -> Tuple[List[Node], int]:
    """Generate the list of metadata nodes used for password recovery."""
    state = seed
    # Choose password length between 6 and 10
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
        # col_disp corresponds to offset of col_val field in C struct
        col_disp = 0  # placeholder; not used directly here
        # noise: combine two random 32-bit values into 64-bit
        state, low = lcg_next(state)
        state, high = lcg_next(state)
        noise = (high << 32) | low
        nodes.append(Node(position, row_index, col_val, col_disp, valid, contributes, noise))
    return nodes, length


def recover_password(nodes: List[Node], vault: List[List[str]]) -> str:
    """Recover the password string from nodes and vault."""
    # Determine maximum position to allocate output
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


def compute_expected_password(student_id: str) -> str:
    """Compute the expected password for a given student ID."""
    seed = compute_seed(student_id)
    vault = generate_vault(seed)
    nodes, _ = generate_nodes(seed)
    return recover_password(nodes, vault)


class Y86Simulator:
    def __init__(self, program_lines: List[str], array: List[int], target: int):
        # Registers are named r0..r14; initialise to zero
        self.regs: Dict[str, int] = {f'r{i}': 0 for i in range(15)}
        self.ZF: bool = False
        # Memory maps labels to values or lists
        self.memory: Dict[str, Union[int, List[int]]] = {
            'array': array,
            'len': len(array),
            'target': target,
        }
        # Parse program and map labels to instruction indices
        self.program: List[Tuple[str, List[str]]] = []  # list of (op, args)
        self.labels: Dict[str, int] = {}
        self._parse(program_lines)
        # Program counter
        self.PC: int = 0

        # Preload registers with array pointer, length, and target code.
        #
        # Before the student's program begins execution, the simulator places the
        # address of the array into %r1, the length of the array into %r2, and
        # the target code into %r3.  The pointer is represented by the label
        # name (a string), so that memory loads use the appropriate label.
        self.regs['r1'] = 'array'
        self.regs['r2'] = len(array)
        self.regs['r3'] = target

    def _parse(self, lines: List[str]) -> None:
        """Parse assembly lines into instructions and labels."""
        for idx, line in enumerate(lines):
            # Remove comments
            if '#' in line:
                line = line[: line.index('#')]
            line = line.strip()
            if not line:
                continue
            # Check for label
            if ':' in line:
                parts = line.split(':', 1)
                label = parts[0].strip()
                if label:
                    # Associate label with next instruction index
                    self.labels[label] = len(self.program)
                remainder = parts[1].strip()
                if remainder == '':
                    continue
                # There is an instruction on the same line after the colon
                line = remainder
            # Split opcode and operands
            tokens = line.split(None, 1)
            op = tokens[0].strip()
            args: List[str] = []
            if len(tokens) > 1:
                argstr = tokens[1]
                # Split arguments on commas that are not inside parentheses
                import re as _re  # local alias for regex
                parts = _re.split(r',(?![^()]*\))', argstr)
                args = [arg.strip() for arg in parts if arg.strip()]
            self.program.append((op, args))

    def _get_reg(self, name: str) -> int:
        """Retrieve register value by name (with leading `%`)."""
        if name.startswith('%'):
            name = name[1:]
        if name not in self.regs:
            raise ValueError(f'Unknown register {name}')
        return self.regs[name]

    def _set_reg(self, name: str, value: int) -> None:
        if name.startswith('%'):
            name = name[1:]
        if name not in self.regs:
            raise ValueError(f'Unknown register {name}')
        self.regs[name] = value

    def _load_mem(self, base: Union[int, str], offset: int) -> int:
        """Load a quadword from memory.  Base may be integer or label string."""
        if isinstance(base, int):
            # For simplicity, integer base addresses are not used in this project
            raise ValueError('Integer base addressing not supported')
        label = base
        if label not in self.memory:
            raise KeyError(f'Unknown memory label {label}')
        obj = self.memory[label]
        if isinstance(obj, list):
            # Each element occupies 8 bytes
            idx = offset // 8
            if idx < 0 or idx >= len(obj):
                raise IndexError(f'Memory access out of range for {label} at index {idx}')
            return obj[idx]
        else:
            # Scalar value
            if offset != 0:
                raise ValueError(f'Cannot apply offset {offset} to scalar {label}')
            return obj

    def run(self) -> Tuple[int, int, bool]:
        """Execute the program and return (result, target, opened)."""
        steps = 0
        max_steps = 10000  # safeguard against infinite loops
        while self.PC < len(self.program):
            if steps > max_steps:
                raise RuntimeError('Execution exceeded maximum instruction count')
            steps += 1
            op, args = self.program[self.PC]
            # print debugging? – removed for final build
            if op == 'halt':
                break
            if op == 'irmovq':
                # Two forms: $imm, %rB  or label, %rB
                if len(args) != 2:
                    raise SyntaxError('irmovq requires 2 operands')
                src, dest = args
                # Remove any leading $ and % characters
                if src.startswith('$'):
                    imm_str = src[1:]
                    if imm_str.isdigit() or (imm_str and imm_str[0] == '-' and imm_str[1:].isdigit()):
                        imm_val = int(imm_str)
                        self._set_reg(dest, imm_val)
                    else:
                        # immediate preceded by $ but referencing label
                        self._set_reg(dest, imm_str)
                else:
                    # src is a label name
                    self._set_reg(dest, src)
                self.PC += 1
                continue
            elif op == 'rrmovq':
                if len(args) != 2:
                    raise SyntaxError('rrmovq requires 2 operands')
                src, dest = args
                val = self._get_reg(src)
                self._set_reg(dest, val)
                self.PC += 1
                continue
            elif op == 'addq':
                if len(args) != 2:
                    raise SyntaxError('addq requires 2 operands')
                src, dest = args
                a = self._get_reg(src)
                b = self._get_reg(dest)
                res = b + a
                self._set_reg(dest, res)
                self.ZF = (res == 0)
                self.PC += 1
                continue
            elif op == 'subq':
                if len(args) != 2:
                    raise SyntaxError('subq requires 2 operands')
                src, dest = args
                a = self._get_reg(src)
                b = self._get_reg(dest)
                res = b - a
                self._set_reg(dest, res)
                self.ZF = (res == 0)
                self.PC += 1
                continue
            elif op == 'mrmovq':
                if len(args) != 2:
                    raise SyntaxError('mrmovq requires 2 operands')
                src, dest = args
                # Support three addressing forms:
                # 1. D(%rA)               – constant displacement from base register.
                # 2. D(%rA,%rB)           – constant + register‑computed offset.
                # 3. (%rA,%rB)            – register‑computed offset only (implicit zero constant).
                # Try form 2 first: D(%rA,%rB)
                m = re.match(r'(-?\d+)\((%?\w+),(%?\w+)\)', src)
                if m:
                    off_const_str, base_reg, off_reg = m.groups()
                    off_const = int(off_const_str)
                    base_val = self._get_reg(base_reg)
                    off_val = self._get_reg(off_reg)
                    val = self._load_mem(base_val, off_const + off_val)
                    self._set_reg(dest, val)
                    self.PC += 1
                    continue
                # Form 3: (%rA,%rB)
                m = re.match(r'\((%?\w+),(%?\w+)\)', src)
                if m:
                    base_reg, off_reg = m.groups()
                    base_val = self._get_reg(base_reg)
                    off_val = self._get_reg(off_reg)
                    val = self._load_mem(base_val, off_val)
                    self._set_reg(dest, val)
                    self.PC += 1
                    continue
                # Form 1: D(%rA)
                m = re.match(r'(-?\d+)\((%?\w+)\)', src)
                if m:
                    off_const_str, reg = m.groups()
                    offset = int(off_const_str)
                    base = self._get_reg(reg)
                    val = self._load_mem(base, offset)
                    self._set_reg(dest, val)
                    self.PC += 1
                    continue
                raise SyntaxError(f'Invalid mrmovq operand {src}')
            elif op == 'andq':
                # Bitwise AND: dest = dest & src
                if len(args) != 2:
                    raise SyntaxError('andq requires 2 operands')
                src, dest = args
                a = self._get_reg(src)
                b = self._get_reg(dest)
                # Only integers are supported for bitwise operations
                if isinstance(a, str) or isinstance(b, str):
                    raise TypeError('andq requires numeric registers')
                res = b & a
                self._set_reg(dest, res)
                self.ZF = (res == 0)
                self.PC += 1
                continue
            elif op == 'jmp':
                if len(args) != 1:
                    raise SyntaxError('jmp requires 1 operand')
                label = args[0]
                if label not in self.labels:
                    raise KeyError(f'Unknown label {label}')
                self.PC = self.labels[label]
                continue
            elif op == 'je':
                if len(args) != 1:
                    raise SyntaxError('je requires 1 operand')
                label = args[0]
                if self.ZF:
                    if label not in self.labels:
                        raise KeyError(f'Unknown label {label}')
                    self.PC = self.labels[label]
                else:
                    self.PC += 1
                continue
            elif op == 'jne':
                if len(args) != 1:
                    raise SyntaxError('jne requires 1 operand')
                label = args[0]
                if not self.ZF:
                    if label not in self.labels:
                        raise KeyError(f'Unknown label {label}')
                    self.PC = self.labels[label]
                else:
                    self.PC += 1
                continue
            else:
                raise SyntaxError(f'Unsupported instruction {op}')
        # End of while
        # After halt or program end, gather results
        final_code = self.regs['r4']
        target_code = self.regs['r3']
        opened = (final_code == target_code)
        return final_code, target_code, opened


def main() -> None:
    """Entry point for the simulator.

    Usage:
        python y86_sim.py <program.y86> [STUDENT_ID] [PASSWORD]

    The optional PASSWORD parameter allows you to enter the Part 1 password.  If
    provided and correct for the given student identifier, the target code in
    memory matches the computed result, enabling the vault to open.  If omitted
    or incorrect, the target code is offset by one, preventing the vault from
    opening even if the assembly program computes the correct result.
    """
    # Expect 2–4 arguments: script name, program file, student ID, optional password
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('Usage: python y86_sim.py <program.y86> [STUDENT_ID] [PASSWORD]')
        sys.exit(1)
    program_file = sys.argv[1]
    # Acquire student ID
    if len(sys.argv) >= 3:
        student_id = sys.argv[2]
    else:
        student_id = input('Enter student ID: ').strip()
    # Acquire optional password
    provided_password: str = ''
    if len(sys.argv) == 4:
        provided_password = sys.argv[3]
    try:
        with open(program_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError as e:
        print(f'Error reading program file: {e}')
        sys.exit(1)
    # Compute deterministic array and result from seed
    seed = compute_seed(student_id)
    array, result_code = generate_array_and_result(seed)
    # Determine whether the provided password matches the expected one
    is_correct_password = False
    if provided_password:
        try:
            expected_password = compute_expected_password(student_id)
            is_correct_password = (provided_password.strip() == expected_password)
        except Exception:
            is_correct_password = False
    # Determine target based on password correctness
    if is_correct_password:
        target = result_code
    else:
        # Offset by 1 when password is missing or incorrect to force a mismatch
        target = result_code + 1
    sim = Y86Simulator(lines, array, target)
    try:
        final_code, target_code, opened = sim.run()
    except Exception as ex:
        print(f'Runtime error: {ex}')
        sys.exit(1)
    # Report results
    print('--- Vault Control System ---\n')
    print(f'Final Code: {final_code}')
    print(f'Target Code: {target_code}\n')
    if opened:
        print('VAULT OPEN')
        if is_correct_password:
            print('Congrats, you unlocked 20% of your grade.')
        else:
            # This case should not occur because incorrect password results in mismatched target
            print('Warning: Vault opened without correct password.')
    else:
        if not provided_password:
            print('VAULT LOCKED')
            print('Hint: Provide the password from Part 1 to unlock.')
        elif not is_correct_password:
            print('VAULT LOCKED')
            print('The provided password is incorrect.  The vault remains closed.')
        else:
            print('VAULT LOCKED')
            print('The vault remains closed.')


if __name__ == '__main__':
    main()
