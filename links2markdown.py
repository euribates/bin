#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

page = requests.get("http://www-test.parcan.es/transparencia/contratos/")
sp = BeautifulSoup(page.text, features="html5lib")

for link in sp.find_all('a', string=True):
    url = link.get('href')
    if not url.startswith('http'):
        url = f'http://www-test.parcan.es{url}'
    txt = link.next_element
    print(f' - [{txt}]({url})')
