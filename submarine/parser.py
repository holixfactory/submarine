# -*- coding: UTF-8 -*-

from __future__ import division, unicode_literals
import sys
import re
import os
import chardet # For non-Unicode encoding detection
import pdb

def parser(file, path):
    ext = path.rfind(".")
    converted_path = path[:ext]+".vtt"
    sbt_obj = file.read()
    first_line = sbt_obj
    file.close()
    if first_line[:7] == '<SAMI>\n':
        smi_obj = sbt_obj
        # Remove language class tag
        smi_obj = re.sub('(<P \w >)+', '', smi_obj)
        # Remove all non-numbers in SYNC tag
        smi_obj = re.sub('','',smi_obj)
        # Find empty lines ('&nbsp;') and move the ms marker
        # If the actual subtitle is on the same line as the timestamp, then add a break (\n)
        sbtl = re.search('',smi_obj)
        if len(sbtl) >= 1:
            smi_obj = re.sub('','',smi_obj)
        # Replace '<br>' with '\n'
        smi_obj = re.sub('(<br>)+', '\n', smi_obj)
        # Convert ms into timestamp

    elif first_line[:2] == '1\n' or first_line[:2] == '1\r' or first_line[1:3] == '1\n' or first_line[1:3] == '1\r':
        srt_obj = sbt_obj
        # Convert the timestamp format
        org_ts = re.findall('(\d{0,2}?:\d{0,2}?:\d{0,2}?,)+', srt_obj)
        mod_ts = [a.replace(',','.') for a in org_ts]
        i = 0
        for org in org_ts:
            org = org_ts[i]
            mod = mod_ts[i]
            srt_obj = srt_obj.replace(org, mod)
            i += 1
        # Add string "WEBVTT" at the top
        header = "WEBVTT\n\n"
        srt_obj = header + srt_obj
        if sys.version_info <= (2,8):
            srt_obj = unicode(srt_obj).encode("utf-8")
        with open(converted_path, "w") as converted:
            converted.write(srt_obj)
        if converted:
            converted.close()
            print("Successfully converted the subtitle!")

    else:
        print("Not a valid SAMI or SubRip file!")