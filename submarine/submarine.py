#!/usr/bin/env python

import os
import codecs
import sys
from parser import parser
import chardet # For non-unicode encoding detection

# Usage
usage = """
The Submarine Project. Copyright 2014 TNTcrowd Co., Ltd.\n
This is a Python 2/3 compatible subtitle converter.
This module converts SAMI or SubRip files to a WEBVTT format.\n
Usage --> submarine file_name.srt"""

def main():
    if len(sys.argv) <= 1:
        print(usage)
    else:
        for path in sys.argv[1:]:
            file = open(path, "rb")
            chdt = chardet.detect(file.read())
            if chdt['encoding'] != "utf-8" or chdt['encoding'] != "ascii":
                file.close()
                file = codecs.open(path, "r", encoding=chdt['encoding'])
            parser(file, path)

if __name__ == '__main__':
    main()
