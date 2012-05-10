# -*- coding: utf-8 -*-

# for Python 2.5
from __future__ import with_statement, print_function, unicode_literals

# 3rd party module
from lxml import etree

# standard module
import re
import sys

if sys.version_info[0] == 2:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO

codec = "utf-8"

def main(filename):
    with open(filename, 'rb') as f:
        data = StringIO(f.read().decode(codec))
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


chapter_notation = re.compile("""
\A\*{1,3}
""", re.VERBOSE)
def convert_chapter(notation):
    pass
    

hyperlink_notation = re.compile("""
\[
(?P<url>(https?|ftp)://[\S].+?)
(:title=?(?P<title>.+?))?
(?P<bookmark>:bookmark)?
(?P<image>:image)?
\]
""", re.VERBOSE)

def convert_link(notation):
    """
    convert hyperlink notation into external link directive
    """
    matched = hyperlink_notation.search(notation)
    if matched:
        content = matched.groupdict()
        url = content['url']
        bookmark = content['bookmark']
        image = content['image']
        title = content['title']
    else:
        url, title, bookmark, image = None, None, None, None
    
    if url and title:
        return "`%s <%s>`_" % (title, url)
    elif url and not title:
        return "`%s`_" % (url,)
    else:
        return notation


list_notation = re.compile("""
^(\s+)?\-{1,3}
""", re.VERBOSE)
def convert_list(notation):
    
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
