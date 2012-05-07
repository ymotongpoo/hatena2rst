# -*- coding: utf-8 -*-

# for Python 2.5
from __future__ import with_statement

# 3rd party module
from lxml import etree

# standard module
import re
import sys
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

codec = "utf-8"

def main(filename):
    with open(filename, 'rb') as f:
        data = StringIO(f.read())
        tree = etree.parse(data, etree.XMLParser())
        parse_hatena_xml(tree)

def parse_hatena_xml(tree):
    """
    parse element tree of Hatena diary archived XML tree
    """
    pass


def parse_day(day):
    """
    parse <day> tag
    """
    pass


def parse_body(body):
    """
    parse <body> tag
    """
    pass


def convert_link(notation):
    return notation


def convert_list():
    pass


def convert_img():
    pass


def convert_super_pre():
    """
    convert super pre notation into code-block directive
    """
    pass
    

if __name__ == '__main__':
    from argparse import ArgumentParser

    prog = "hatena2rst"
    description = "Hatena diary XML to reST converter"
    argparse = ArgumentParser(prog=prog, description=description)

    parser.add_argument("filename", type=str)
    args = vars(parser.parse_args())

    main(args.filename)
