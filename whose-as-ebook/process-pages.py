#!/usr/bin/env python3

import argparse
from pathlib import Path

import lxml.html


def process_html_file(in_file, out_file, parser):
    etree = lxml.html.parse(in_file.as_posix(), parser)
    heading = etree.xpath('//h1[@id="firstHeading"]')[0]
    content = etree.xpath('//div[@id="mw-content-text"]')[0]
    with open(out_file, 'w') as fh:
        fh.write(lxml.html.tostring(heading).decode("UTF-8"))
        fh.write(lxml.html.tostring(content).decode("UTF-8"))


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=False, dest='input',
                        default="./whose/web/", help="Path to input directory")
    parser.add_argument('-o', '--output', required=True, dest="output",
                        help="Path to output directory")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    Path(args.output).mkdir(parents=True, exist_ok=True)
    parser = lxml.html.HTMLParser()

    for file_ in Path(args.input).glob("*.html"):
        outfile = Path(args.output).joinpath(file_.name)
        process_html_file(file_, outfile, parser)
