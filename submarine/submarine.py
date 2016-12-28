#!/usr/bin/env python

import sys
from .parser import parser

# Usage
usage = """
The Submarine Project. Copyright 2014-2016 TNTcrowd Co., Ltd.\n
This is a Python 3 subtitle converter.
This module converts SAMI or SubRip files to a WEBVTT format.\n
Usage (If path_to_file is empty, output directory will be the origin of source file):\n
submarine file_name.srt path_to_file.vtt
submarine file_name.smi path_to_file.vtt
"""

def main():
    if len(sys.argv) <= 1:
        print(usage)
    else:
        path_in = sys.argv[1]
        if len(sys.argv) == 3:
            path_out = sys.argv[2]
            parser(path_in, path_out)
        elif len(sys.argv) == 2:
            ext = path_in.rfind('.')
            path_out = path_in[:ext] + ".vtt"
            parser(path_in, path_out)
        else:
            print("Invalid request. See usage!\n" + usage)

if __name__ == '__main__':
    main()
