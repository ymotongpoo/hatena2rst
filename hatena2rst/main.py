# -*- coding: utf-8 -*-

# for Python 2.5
from __future__ import with_statement, print_function, unicode_literals

# 3rd party module
from lxml import etree

# standard module
import re
import sys
import string

if sys.version_info[0] == 2:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO

codec = "utf-8"
indent = "   "

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


section_notation = re.compile("""
\A\s*(?P<notation>\*{2,3})\s*(?P<title>.*)
""", re.VERBOSE)

def convert_section(line):
    matched = section_notation.search(line)
    if matched:
        content = matched.groupdict()
        if content['notation'] == "**":
            division = '='
        else:
            division = '-'
        length = len(content['title'].encode(codec))
        return "%s\n%s" % (content['title'], division * length)
    else:
        return line
    

hyperlink_notation = re.compile("""
\[
(?P<url>(https?|ftp)://[\S].+?)
(:title=?(?P<title>.+?))?
(?P<bookmark>:bookmark)?
(?P<image>:image)?
\]
""", re.VERBOSE)

def convert_link(line):
    """
    convert hyperlink notation into external link directive

    TODO: add procedure for image and bookmark
    TODO: add function for getting title when no title specified
    """
    target = line
    for m in hyperlink_notation.finditer(line):
        notation = m.group(0)
        content = m.groupdict()
        url = content['url']
        bookmark = content['bookmark']
        image = content['image']
        title = content['title']
    
        if url and title:
            converted = " `%s <%s>`_ " % (title, url)
        elif url and not title:
            converted = " `%s`_ " % (url,)
        target = target.replace(notation, converted)

    return target.strip()


list_notation = re.compile("""
\A\s*(?P<depth>\-{1,3})(?P<content>.*)
""", re.VERBOSE)

def convert_list(line):
    matched = list_notation.search(line)
    prefix = ""
    if matched:
        content = matched.groupdict()
        print(content)
        if content['depth']:
            prefix = indent * ( len(content['depth']) - 1 ) + '*'
        return "%s %s" % (prefix, content['content'])
    else:
        return line
    

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
