#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import Counter

from tqdm import tqdm
from rich.console import Console
from rich.table import Table
import typer

extensions = {
    '.py': 'Python',
    '.css': 'CSS Stylesheets',
    '.js': 'Javascript',
    '.html': 'Html'
}


def count_lines(filename: str) -> int:
    '''Devuelve el total de líneas con código de un fichero.
    '''
    result = 0
    with open(filename, 'r', encoding='utf-8') as f_in:
        try:
            for line in f_in:
                if line.strip() == '':
                    continue
                result += 1
        except UnicodeDecodeError as err:
            print(f'Error: {err}')
            print(f'Fichero: {filename}')
            return 0
    return result


def show_stats(base, num_files, num_lines):
    '''Imprime las estadísticas de nº de archivos y líneas por tipo de archivo.
    '''
    table = Table(title=f"Estadisticas {base}")
    table.add_column("Tipo", style="cyan", no_wrap=True)
    table.add_column("N. archivos", justify="right")
    table.add_column("N. líneas", justify="right")
    for ext in extensions:
        desc = extensions[ext]
        table.add_row(
            desc,
            str(num_files[ext]),
            str(num_lines[ext]),
            )
    console = Console()
    console.print(table)


def main(base='.'):
    num_files = Counter()
    num_lines = Counter()
    for (dirname, _directories, files) in tqdm(os.walk(base)):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext in extensions:
                num_files[ext] += 1
                full_path = os.path.join(dirname, file)
                num_lines[ext] += count_lines(full_path)
    show_stats(base, num_files, num_lines)


if __name__ == "__main__":
    typer.run(main)
