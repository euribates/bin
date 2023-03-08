#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from collections import Counter


def main():
    stats = Counter()
    for file_name in sys.stdin:
        pth = Path(file_name)
        stats[pth.parts[0]] += 1
    for name in sorted(stats):
        print(name, stats[name])


if __name__ == "__main__":
    main()
