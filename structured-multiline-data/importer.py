#!/usr/bin/env python3

import re
import sys
import csv

def trim(string):
    return re.sub(r'\s+', ' ', string.strip())

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

            self.content.append([trim(e) for e in elems.groups()])

    def writeCSV(self, where):
        csvfile = where
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(self.content)

for filename in sys.argv[1:]:
    top = TopList(filename)
    top.writeCSV(sys.stdout)
