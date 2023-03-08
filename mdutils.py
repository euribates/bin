#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import re


def get_title_from_url(url):
    pat_title = re.compile(
        r"<title>"
        "(.+?)"
        "</title>",
        re.IGNORECASE | re.DOTALL
        )
    req = requests.get(url)
    match = pat_title.search(req.text)
    if match:
        return match.group(1)
    return ''


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else 'http://www.parcan.es/'
    title = get_title_from_url(url) or url
    print(f"[{title}]({url})")


if __name__ == '__main__':
    main()
