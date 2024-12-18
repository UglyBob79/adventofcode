#!/usr/bin/env python3
import re
from copy import deepcopy

re_regs = re.compile(r"Register (\w): (\d+)")
re_prog = re.compile(r"Program: (.*)")

def combo(cpu, operand):
    if operand <= 3:
        return operand
    elif operand == 4:
        return cpu['regs']['A']
    elif operand == 5:
        return cpu['regs']['B']
    elif operand == 6:
        return cpu['regs']['C']
    else:
        print("ERROR")
        return None

def combo_str(cpu, operand):
    if operand <= 3:
        return str(operand)
    elif operand == 4:
        return "reg[A]"
    elif operand == 5:
        return "reg[B]"
    elif operand == 6:
        return "reg[C]"
    else:
        return "ERR"

def print_prog(prog):
    ptr = 0

    while ptr < len(prog):
        opcode = prog[ptr]
        operand = prog[ptr + 1]

        if opcode == 0:
            print(f"adv: reg[A] = reg[A] // 2^{combo_str(cpu, operand)}")
        elif opcode == 1:
            print(f"bxl: reg[B] = reg[B] ^ {operand}")
        elif opcode == 2:
            print(f"bst: reg[B] = {combo_str(cpu, operand)} % 8")
        elif opcode == 3:
            print(f"jnz: jump reg[A]!=0: {operand}")
        elif opcode == 4:
            print(f"bxc: reg[B] = reg[B] ^ reg[C]")
        elif opcode == 5:
            print(f"out: output {combo_str(cpu, operand)} % 8")
        elif opcode == 6:
            print(f"bdv: reg[B] = reg[A] // 2^{combo_str(cpu, operand)}")
        elif opcode == 7:
            print(f"cdv: reg[C] = reg[A] // 2^{combo_str(cpu, operand)}")

        ptr += 2

def run_program(cpu):
    out = []
    while cpu['ptr'] < len(cpu['prog']):
        opcode = cpu['prog'][cpu['ptr']]
        operand = cpu['prog'][cpu['ptr'] + 1]

        if opcode == 0: # adv (division A)
            numerator = cpu['regs']['A']
            divisor = 1 << combo(cpu, operand)
            cpu['regs']['A'] = numerator // divisor
        elif opcode == 1: # bxl (bitwise B xor operand)
            cpu['regs']['B'] ^= operand
        elif opcode == 2: # bst (modulo 8)
            cpu['regs']['B'] = combo(cpu, operand) % 8
        elif opcode == 3: # jnz (jump)
            if cpu['regs']['A'] != 0:
                cpu['ptr'] = operand
                continue
        elif opcode == 4: # bxc (bitwise A xor B)
            cpu['regs']['B'] ^= cpu['regs']['C']
        elif opcode == 5: # out (output)
            out.append(combo(cpu, operand) % 8)
        elif opcode == 6: # bdv (adv with B)
            numerator = cpu['regs']['A']
            divisor = 1 << combo(cpu, operand)
            cpu['regs']['B'] = numerator // divisor
        elif opcode == 7: # cdv (adv with C)
            numerator = cpu['regs']['A']
            divisor = 1 << combo(cpu, operand)
            cpu['regs']['C'] = numerator // divisor

        cpu['ptr'] += 2

    return out

def reset(cpu):
    for reg in cpu['regs']:
        cpu['regs'][reg] = 0
    cpu['ptr'] = 0

with open("17.input") as file:
    cpu = {'regs': {}, 'prog': [], 'ptr': 0}

    for line in file:
        line = line.strip()
        if not line:
            continue

        match = re_regs.match(line)
        if match:
            cpu['regs'][match.group(1)] = int(match.group(2))
        else:
            match = re_prog.match(line)
            if match:
                cpu['prog'] = [int(v) for v in match.group(1).split(",")]

    print(','.join(map(str, run_program(cpu))))

    reset(cpu)
    solutions = [0]
    found_a = None

    for item in reversed(cpu['prog']):
        new_solutions = []
        for solution in solutions:
            for a in range(8):
                test_a = solution << 3 | a
                cpu['regs']['A'] = test_a
                cpu['ptr'] = 0

                out = run_program(cpu)

                if out[0] == item:
                    new_solutions.append(test_a)
                    if not found_a and cpu['prog'] == out:
                        found_a = test_a
                        break
        solutions = new_solutions

    print(found_a)
