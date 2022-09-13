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
    nodes_accepted_before_try = (
        ast.Assign,
        ast.ClassDef,
        ast.FunctionDef,
        ast.Import,
        ast.ImportFrom,
    )
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename)
    except SyntaxError as err:
        return False, "Error sintáctico en el código fuente: {err}"
    nodes = list(tree.body)
    if not nodes:
        return False, "No hay código, árbol AST vacío"
    all_first_statements_are_valid = all(
        isinstance(n, nodes_accepted_before_try)
        for n in nodes[0:-1]
        )
    if not all_first_statements_are_valid:
        return False, "No todas las sentencias anteriores al try son válidas"
    last_statement_is_try = isinstance(nodes[-1], ast.Try)
    if not last_statement_is_try:
        return False, "La últioma sentencia no es un try"
    return True, ''


def main():
    parser = get_parser()
    args = parser.parse_args()
    prefix = ''
    for arg_filename in args.filenames:
        filename = Path(arg_filename)
        if not filename.exists():
            continue
        is_ready, error_message = source_is_reliable(filename)
        if is_ready:
            if args.files:
                print(prefix, filename, end="")
                prefix = "\n"
            else:
                print('filename', filename, OK)
        else:
            print('filename', filename, ERROR, error_message)



if __name__ == "__main__":
    main()
