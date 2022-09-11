#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import ast
import os
import pathlib
import re
import sys

OK = "\u001b[32m[OK]\u001b[0m"
SKIPPED = "\u001b[33m[Skipped]\u001b[0m"
FIXED = "\u001b[32m[Fixed]\u001b[0m"
ERROR = "\u001b[31m[Nope]\u001b[0m"


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filenames', type=str, nargs='+', help='Files to fix')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--check', action='store_true')
    return parser


def read_file_lines(filename) -> []:
    with open(filename, 'r') as f:
        lines = [l.rstrip() for l in f.readlines()]
    return lines


def main_function_exists(lines):
    pat_main = re.compile(r"def main\(\):")
    for line in lines:
        if pat_main.match(line):
            return True
    return False


def is_import_line(line):
    return any([
        'import' in line,
        line.startswith('#'),
    ])


def find_try_statement(lines, filename):
    tree = ast.parse('\n'.join(lines), filename)
    for node in tree.body:
        if isinstance(node, ast.Try):
            return node.lineno - 1
    raise ValueError(f"Imposibe encontrar la sentencia Try en {filename}")


def split_code(lines, filename):
    imports = []
    body = []
    last_import_line = find_try_statement(lines, filename)
    for num_line, line in enumerate(lines):
        if num_line < last_import_line:
            imports.append(line)
        else:
            body.append(line)
    return imports, body


def generate_new_code(imports, body, output=sys.stdout):
    for line in imports:
        print(line, file=output)
    print("\n", file=output)
    print('def main():', file=output)
    for line in body:
        if line.strip() == '':
            print(file=output)
        else:
            print(f"    {line}", file=output)
    print("\n", file=output)
    print("if __name__ == '__main__':", file=output)
    print("    main()", file=output)



def main():
    parser = get_parser()
    args = parser.parse_args()
    for arg_filename in args.filenames:
        filename = pathlib.Path(arg_filename)
        print('filename', filename, end=" ")
        lines = read_file_lines(filename)
        workable = not main_function_exists(lines)
        if args.check:
            print(OK if workable else ERROR)
            continue
        if workable:
            imports, body = split_code(lines, arg_filename)
            if args.force:
                backup_filename = filename.with_suffix(f".old")
                if not backup_filename.exists():
                    filename.rename(backup_filename)
                filename = pathlib.Path(arg_filename)
                with filename.open("w") as f:
                    generate_new_code(imports, body, output=f)
                os.chmod(filename, 0o755)
                print(FIXED)
            else:
                generate_new_code(imports, body)
                print(SKIPPED)
            continue


if __name__ == "__main__":
    main()
