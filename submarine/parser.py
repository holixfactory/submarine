import sys
import re
import os
import codecs
import chardet # For non-unicode encoding detection
import logging

from .samiparser import SAMIParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stderr))


def parser(path_in, path_out):
    """
    :param path_in: SAMI or SubRip style subtitle file path.
    :param path_out: WEBVTT file path.
    :return: True if process finished well, False otherwise.
    """

    if not os.path.exists(path_in):
        logger.error('File does not exist! Please check the directory.\n')
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
        parser = SAMIParser()

        parser.feed(sbt_obj)
        parser.build_parsed()
        parsed = parser.PARSED

        with open(path_out, "w") as converted:
            converted.write(parsed)
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
        with open(path_out, "w") as converted:
            converted.write(srt_obj)
        if converted:
            converted.close()
            print("Successfully converted the subtitle!")
    else:
        logger.error("The file is either corrupted or not a valid SAMI or SubRip file!")
        return False

    return True
