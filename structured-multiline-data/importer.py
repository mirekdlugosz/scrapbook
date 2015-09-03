#!/usr/bin/env python3

import re
import sys
import csv

class TopList():
    def __init__(self, filename):
        self.filename = filename
        self.content = []
        self.content.append(["This Week", "Last Week", "Song Title",
            "Artist", "Label", "Weeks on Chart", "Peak Position"])
        self.read()

    def read(self):
        fileContent = open(self.filename, 'r').read()
        fileContent = re.sub(r'\n(\t? {4,})', '\t', fileContent)
        for line in fileContent.split('\n'):
            elems = re.compile(
                    r'^\s*(\d+)'
                    r'\s*(\d+|--)'
                    r'\s*(.+?)'
                    r'\t(.+)'
                    r'\s+\((.+)\)'
                    r'-(\d+)'
                    r'\s.*\((\d+)\)$'
                ).match(line)
            if not elems:
                continue
            self.content.append([elems.group(1), elems.group(2), elems.group(3), 
                elems.group(4), elems.group(5), elems.group(6), elems.group(7)])

    def writeCSV(self, where):
        csvfile = where
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(self.content)

for filename in sys.argv[1:]:
    top = TopList(filename)
    top.writeCSV(sys.stdout)
