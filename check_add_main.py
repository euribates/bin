#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import argparse
import ast

OK = "\u001b[32m[OK]\u001b[0m"
ERROR = "\u001b[31m[Nope]\u001b[0m"

def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filenames', type=str, nargs='+', help='Files to fix')
    parser.add_argument('-f', '--files', action='store_true')
    return parser


def source_is_reliable(filename: str or Path) -> bool:
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename)
    except SyntaxError:
        return False
    nodes = list(tree.body)
    if not nodes:
        return False
    all_first_statements_are_imports = all(
        isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        for n in nodes[0:-1]
        )
    last_statement_is_try = isinstance(nodes[-1], ast.Try)
    return all_first_statements_are_imports and last_statement_is_try


def main():
    parser = get_parser()
    args = parser.parse_args()
    prefix = ''
    for arg_filename in args.filenames:
        filename = Path(arg_filename)
        if not filename.exists():
            continue
        is_ready = source_is_reliable(filename)
        if args.files:
            if is_ready:
                print(prefix, filename, end="")
                prefix = "\n"
        else:
            print('filename', filename, end=" ")
            print (OK if is_ready else ERROR)


if __name__ == "__main__":
    main()
