import sys
import os
import codecs
import chardet

from html.parser import HTMLParser

class SAMIParser(HTMLParser):
    parsed_list = []
    PARSED = "WEBVTT\n\n"

    def handle_starttag(self, tag, attrs):
        if tag == "sync":
            self.parsed_list.append(int(attrs[0][1]))
        elif tag == "font":
            self.parsed_list.append("font")

    def handle_data(self, data):
        if len(self.parsed_list) > 0 and self.parsed_list[-1] == "font":
            self.parsed_list.pop()
            self.parsed_list[-1] += data
        else:
            self.parsed_list.append(data)

    def handle_endtag(self, tag):
        if tag == "head":
            self.parsed_list.append(tag)

    def ms_to_hhmmssms(self, ms):
        ms = int(ms)
        hh = ms // 3600000
        ms = ms % 3600000
        mm = ms // 60000
        ms = ms % 60000
        ss = ms // 1000
        ms = ms % 1000
        return '%02d:%02d:%02d.%03d' % (hh, mm, ss, ms)

    def build_parsed(self):
        head = True

        while head:
            current = self.parsed_list.pop(0)
            if current == 'head':
                head = False

        line_no = 1
        while self.parsed_list:
            queue = []

            try:
                while str(self.parsed_list[0]).isspace():
                    self.parsed_list.pop(0)

                queue.append(self.parsed_list.pop(0))
            except IndexError:
                continue

            while queue and self.parsed_list:
                cur_parsed = self.parsed_list.pop(0)
                if str(cur_parsed).isspace():
                    continue
                elif isinstance(cur_parsed, int):
                    self.PARSED += str(line_no) + '\n'
                    for element in queue:
                        if isinstance(element, int):
                            self.PARSED += self.ms_to_hhmmssms(element)
                            self.PARSED += " --> "
                            self.PARSED += self.ms_to_hhmmssms(cur_parsed)
                        else:
                            self.PARSED += element

                    self.PARSED += '\n'
                    queue.clear()
                    line_no += 1
                else:
                    queue.append(cur_parsed)
