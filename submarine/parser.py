# -*- coding: UTF-8 -*-

from __future__ import division, unicode_literals
import sys
import re
import codecs
import chardet # For non-unicode encoding detection

def parser(path_in, path_out):
    file = open(path_in, "rb")
    chdt = chardet.detect(file.read())
    if chdt['encoding'] != "utf-8" or chdt['encoding'] != "ascii":
        file.close()
        file = codecs.open(path_in, "r", encoding=chdt['encoding'])
        sbt_obj = file.read()
    else:
        file.close()
        file = open(path_in, 'r')
        sbt_obj = file.read()
    first_line = sbt_obj
    file.close()
    if first_line[:6] == '<SAMI>' or first_line[1:7] == '<SAMI>':
        smi_obj = sbt_obj
        # Create ms list
        ms_list = re.findall('=\d+',smi_obj)
        # Convert ms into timestamp
        ms_list = [a.replace('=','') for a in ms_list]
        ms_list = [int(b) for b in ms_list]
        i = 0
        ts_list = []
        for ms_el in ms_list:
            ms_el = ms_list[i]
            hr = ms_el // 3600000
            ms_el = ms_el % 3600000
            mi = ms_el // 60000
            ms_el = ms_el % 60000
            s = ms_el // 1000
            ms_el = ms_el % 1000
            ms = ms_el
            ts_el = '%02d:%02d:%02d.%03d' % (hr, mi, s, ms)
            ts_list.append(ts_el)
            i += 1
        # Add two timestamps to SubRip format (ts --> ts)
        start = 0
        end = 1
        converted_ts = []
        while end <= len(ts_list):
            ts_el = ts_list[start] + " --> " + ts_list[end]
            converted_ts.append(ts_el)
            start += 2
            end += 2
        content_ls = re.findall('(<sync start=\d+><p class=\w+>(\s|\S){1,255}?<sync start=\d+>)'\
        , smi_obj, flags=re.IGNORECASE)
        j = 0
        converted_ct = []
        while j < len(content_ls):
            content_el = content_ls[j][0]
            content_el = re.sub('\r\n', '', content_el)
            content_el = re.sub('\n', '', content_el)
            content_el = re.sub('<br>', '\n', content_el)
            content_el = re.sub('<sync start=\d+>','', content_el, flags=re.IGNORECASE)
            content_el = re.sub('<p class=\w+>', '', content_el, flags=re.IGNORECASE)
            converted_ct.append(content_el)
            j += 1
        que = 1
        num = 0
        final_obj = "WEBVTT\n\n"
        while num < len(converted_ts):
            if que == len(converted_ts):
                final_obj = final_obj + str(que) +'\n' + converted_ts[num] + '\n' + converted_ct[num]
            else:
                final_obj = final_obj + str(que) +'\n' + converted_ts[num] + '\n' + converted_ct[num] + '\n\n'
            que += 1
            num += 1
        if sys.version_info <= (2,8):
            final_obj = unicode(final_obj).encode("utf-8")
        with open(path_out, "w") as converted:
            converted.write(final_obj)
        if converted:
            converted.close()
            print("Successfully converted the subtitle!")
    elif first_line[:2] == '1\n' or first_line[:2] == '1\r' \
        or first_line[1:3] == '1\n' or first_line[1:3] == '1\r':
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
        with open(path_out, "w") as converted:
            converted.write(srt_obj)
        if converted:
            converted.close()
            print("Successfully converted the subtitle!")
    else:
        print("Not a valid SAMI or SubRip file!")