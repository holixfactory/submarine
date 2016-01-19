# -*- coding: UTF-8 -*-

from __future__ import division, unicode_literals
import sys
import re
import os
import codecs
import chardet # For non-unicode encoding detection


def parser(path_in, path_out):
    """
    :param path_in: SAMI or SubRip style subtitle file path.
    :param path_out: WEBVTT file path.
    :return: True if process finished well, False otherwise.
    """

    if not os.path.exists(path_in):
        sys.stderr.write('File does not exist! Please check the directory.\n')
        return False
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
    first_line = sbt_obj[:10]
    file.close()
    if first_line.find('<SAMI>') != -1:
        smi_obj = sbt_obj
        # Match ms pair
        ms_chk = re.findall('(<sync start=\d+><p class=\w+>(\s|\S){3,255}?(\s))'\
            ,smi_obj, flags=re.IGNORECASE)
        g = 0
        ms_list = []
        if ms_chk[g][0].find('&nbsp;') != -1:
            g += 1
        while g < len(ms_chk):
            if g != len(ms_chk) - 1:
                first = ms_chk[g][0].find('&nbsp;')
                second = ms_chk[g + 1][0].find('&nbsp;')
                if first == -1 and second != -1:
                    first_search = re.search('=\d+',ms_chk[g][0])
                    second_search = re.search('=\d+',ms_chk[g + 1][0])
                    ms_list.append(first_search.group(0))
                    ms_list.append(second_search.group(0))
                    g += 2
                elif first == -1 and second == -1:
                    first_search = re.search('=\d+',ms_chk[g][0])
                    second_search = re.search('=\d+',ms_chk[g + 1][0])
                    ms_list.append(first_search.group(0))
                    ms_list.append(second_search.group(0))
                    g += 1
            elif g == len(ms_chk) - 1:
                first_search = re.search('=\d+',ms_chk[g][0])
                ms_list.append(first_search.group(0))
                g += 1
        ms_list = [a.replace('=','') for a in ms_list]
        # Check if last subtitle has an end
        chk_pair = len(ms_list) % 2
        if chk_pair != 0:
            last_ms = ms_list[len(ms_list) - 1]
            last_ms = int(last_ms) + 2000
            ms_list.append(last_ms)
        # Convert ms into timestamp
        i = 0
        ts_list = []
        for ms_el in ms_list:
            ms_el = ms_list[i]
            hr = int(ms_el) // 3600000
            ms_el = int(ms_el) % 3600000
            mi = int(ms_el) // 60000
            ms_el = int(ms_el) % 60000
            s = int(ms_el) // 1000
            ms_el = int(ms_el) % 1000
            ms = int(ms_el)
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
        content_ls = re.findall('(<p class=\w+>(\s|\S){1,}?<sync)'\
        , smi_obj, flags=re.IGNORECASE)
        break_point = smi_obj.rfind("<P")
        last_ct = smi_obj[break_point:]
        last_ct = re.sub('</body>','', last_ct, flags=re.IGNORECASE)
        last_ct = re.sub('</sami>','', last_ct, flags=re.IGNORECASE)
        content_ls.append(last_ct)
        qwe = 0
        converted_ct = []
        while qwe < len(content_ls):
            if qwe == len(content_ls) - 1:
                content_el = content_ls[qwe]
            else:
                content_el = content_ls[qwe][0]
            content_el = re.sub('\r\n', '', content_el)
            content_el = re.sub('\n', '', content_el)
            content_el = re.sub('<br>', '\n', content_el)
            content_el = re.sub('&nbsp;', '', content_el, flags=re.IGNORECASE)
            content_el = re.sub('<p class=\w+>', '', content_el, flags=re.IGNORECASE)
            content_el = re.sub('<sync','', content_el, flags=re.IGNORECASE)
            converted_ct.append(content_el)
            qwe += 1
        converted_ct = list(filter(bool, converted_ct))
        converted_ct = list(filter(lambda whitespace: whitespace.strip(), converted_ct))
        if len(converted_ts) != len(converted_ct):
            sys.stderr.write("The SAMI file has SYNC tag(s) with no actual caption!\nPlease check your SAMI file!\n")
            return False
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
    elif first_line[:5].find('1') != -1:
        srt_obj = sbt_obj
        # Convert the timestamp format
        org_ts = re.findall('(\d{0,2}?:\d{0,2}?:\d{0,2}?,)+', srt_obj)
        mod_ts = [a.replace(',','.') for a in org_ts]
        i = 0
        for org in org_ts:
            org = org_ts[i]
            mod = mod_ts[i]
            srt_obj = re.sub(org, mod, srt_obj)
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
        print("The file is either corrupted or not a valid SAMI or SubRip file!")
        return False

    return True
