#! /usr/bin/env python

import os
from sys import argv, stdin
from io import open
from parser import parser

# Usage
usage = """
The Submarine Project. Copyright 2014 TNTcrowd Co., Ltd.\n
This is a Python 2/3 compatible subtitle converter.
This module converts SAMI or SubRip files to a WEBVTT format.\n
Usage --> submarine file_name.srt"""

def main():
    if len(argv) <= 1:
        print(usage)
    else:
        for path in argv[1:]:
            with open(path, "r") as file:
                parser(file, path)

if __name__ == '__main__':
    main()