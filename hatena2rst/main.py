# -*- coding: utf-8 -*-

# for Python 2.x
from __future__ import with_statement, print_function, unicode_literals

# 3rd party module
from lxml import etree
import unicodedata

# standard module
import re
import sys
from datetime import datetime

if sys.version_info[0] == 2:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO

from constants import codec, indent, image_extensions, filetype_map


"""
main process
"""
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

"""
utility functions
"""
def string_width(string):
    """
    measure rendered string width.
    take multibyte characters as 2.
    """
    width = 0
    for c in string:
        char_width = unicodedata.east_asian_width(c)
        if char_width in "WFA":
            width += 2
        else:
            width += 1
    return width

"""
convert multi-line notations
  - quate notation (>>..<<)
  - pre notation (>|..|<)
  - super pre notation (>||..||<)
"""

# super pre notatino
#  - http://goo.gl/Q2szA
#  - http://goo.gl/xtQWf
def convert_super_pre(depth, block, filetype):
    """
    convert super pre notation into code-block directive
    """
    indented_block = [ indent*depth + l for l in block ]
    pass
    


"""
convert in-line notations
  - chapter/section notation (*, **, ***)
  - hyperlink notation ([http://...])
  - list notation (-..., +..., etc)
  - id notation (id:user:20120512, etc)
  - fotolive notation ([f:id:user:20120512094500:image], etc)
"""

# chapter notation
#  - http://goo.gl/CDXtj
#  - http://goo.gl/IkpfS
chapter_notation = re.compile("""
\A\s*\*(?P<epoch>[0-9]{9,10})\*\s*(?P<title>.*)
""", re.VERBOSE)

def convert_chapter(line):
    matched = chapter_notation.search(line)
    if matched:
        content = matched.groupdict()
        dt = None
        if content['epoch']:
            dt = datetime.fromtimestamp(int(content['epoch']))
        title = content['title']
        length = string_width(title)
        division = '=' * (length + 2)
        return "%s\n %s \n%s" % (division, title, division)
    else:
        return line

# section notation
#  - http://goo.gl/eZTQu
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
        length = string_width(content['title'])
        return "%s\n%s" % (content['title'], division * length)
    else:
        return line
    
# hyperlink notation
#  - http://goo.gl/m8cS
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
        elif image:
            if url[-3] in image_extensions:
                converted = ""
        target = target.replace(notation, converted)

    return target.strip()

# list notation
#  - http://goo.gl/UpXR7
list_notation = re.compile("""
\A(?P<depth>(\-{1,3}|\+{1,3}))(?P<content>.*)
""", re.VERBOSE)

def convert_list(line):
    markup_map = {"-": "*", 
                  "+": "#."}
    matched = list_notation.search(line)
    prefix = ""
    if matched:
        content = matched.groupdict()
        if content['depth']:
            markup = markup_map[content['depth'][0]]
            prefix = indent * ( len(content['depth']) - 1 ) + markup
        return "%s %s" % (prefix, content['content'])
    else:
        return line

# id notation (diary notation)
#  - http://goo.gl/5nlXD
#  - http://goo.gl/uzUx7
id_notation = re.compile("""
(d:)?id:(?P<user>[\w\-]+)
(:((?P<date>\d{8})|(?P<month>\d{6})|(?P<option>archive|about)))?
((?P<separator>(:|\#))((?P<epoch>\d{9,10})|(?P<amonth>\d{6})))?
""", re.VERBOSE)

diary_url_tmpl = r"http://d.hatena.ne.jp/%s/"

def convert_id(line):
    separator_map = {"#": "#", 
                     ":": "/"}
    target = line
    for m in id_notation.finditer(line):
        notation = m.group(0)
        content = m.groupdict()
        converted = diary_url_tmpl % content['user']
        if content['date']:
            converted += "%s" % content['date']
            if content['epoch']:
                separator = separator_map[content['separator']]
                converted += "%s%s" % (separator, content['epoch'])
        elif content['month']:
            converted += "%s" % content['month']
        elif content['option']:
            converted += "%s" % content['option']
            if content['amonth'] and content['option'] == 'archive':
                converted += "/%s" % content['amonth']
        print((converted, notation))
        converted = "`%s <%s>`_" % (notation, converted)
        target = target.replace(notation, converted)

    return target
    
# fotolife notation
#  - http://goo.gl/yxb8
fotolife_notation = re.compile("""
\[f:id:(?P<user>[0-9a-zA-Z_\-]+?)
(:(?P<dt>\d{14}[a-z]))?
(?P<image>:image)?
(:(?P<option>[a-z0-9,]+))?\]
""", re.VERBOSE)

image_url_tmpl = (r"http://f.hatena.ne.jp/images/fotolife/" +
                  r"%(initial)s/%(user)s/%(date)s/%(dt)s.%(ext)s")

def generate_image_directive(image_url, option):
    directive = ".. image:: %s\n" % image_url
    for k, v in option.items():
        if v:
            directive += "   :%s: %s\n" % (k, v)
    return directive

def get_image_option(option_string):
    option_dict = dict(
        height=None,
        width=None,
        align=None,
        scale=None
        )
    if option_string:
        options = option_string.split(',')
    else:
        options = []
    for o in options:
        if re.search("\A(h|w)\d+", o):
            if o[0] == "h":
                option_dict['height'] = o[1:]
            else:
                option_dict['width'] = o[1:]
        elif o in ['left', 'right']:
            option_dict['align'] = o
        elif o == 'small':
            option_dict['scale'] = '20%'
        elif o == 'medium':
            option_dict['scale'] = '40%'

    return option_dict

def convert_fotolife(line):
    target = line
    for m in fotolife_notation.finditer(line):
        notation = m.group(0)
        content = m.groupdict()
        
        if content['image']:
            """
            TODO: Replace this image url generator with
            Hatena fotolife API. Image urls are fetched
            through GET request to EditURI.
            http://developer.hatena.ne.jp/ja/documents/fotolife/apis/atom
            """
            content['date'] = content['dt'][:8]
            content['initial'] = content['user'][0]
            content['ext'] = 'png'
            image_url = image_url_tmpl % content
            
            option = get_image_option(content['option'])
            converted = generate_image_directive(image_url, option)
            target = target.replace(notation, converted)
        else:
            converted = r"http://f.hatena.ne.jp/" + content['user']
            if content['dt']:
                converted += "/" + content['dt'][:8] + "/" + content['dt']
            converted = "`%s`_" % converted

            target = target.replace(notation, converted)

    return target


if __name__ == '__main__':
    from argparse import ArgumentParser

    prog = "hatena2rst"
    description = "Hatena diary XML to reST converter"
    argparse = ArgumentParser(prog=prog, description=description)

    parser.add_argument("filename", type=str)
    args = vars(parser.parse_args())

    main(args.filename)
