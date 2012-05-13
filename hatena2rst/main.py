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
    from StringIO import StringIO
else:
    from io import StringIO

from constants import codec, indent, status_flag, image_extensions, filetype_map


"""
main process
"""
def main(filename):
    with open(filename, 'rb') as f:
        data = StringIO(f.read())
        tree = etree.parse(data, etree.XMLParser(recover=True))
        results = parse_hatena_xml(tree)
        for day, data in results:
            day_file = day.encode(codec) + ".rst"
            fp = open(day_file, 'wb+')
            fp.write(data.encode(codec))
            fp.close()


def parse_hatena_xml(tree):
    """
    parse element tree of Hatena diary archived XML tree
    """
    days = tree.xpath("//day")
    return [parse_day(d) for d in days]


def parse_day(day):
    """
    parse <day> tag
    """
    date = day.attrib['date']
    title = day.attrib['title']
    body = day.xpath("./body")[0]
    if title:
        header = ":%s: %s\n\n" % (day, title)
        return (date, header + parse_body(body))
    else:
        return (date, parse_body(body))


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
  - quote notation (>>..<<)
  - pre notation (>|..|<)
  - super pre notation (>||..||<)
"""


# quote notation
#  - http://goo.gl/HunQj
quote_sp_start_notation = re.compile("""
\A
(?P<quote>>(?P<site>(https?|ftp)://\S+)?>)|
(?P<sp>>\|(?P<filetype>\w+)?\|)
\Z
""", re.VERBOSE)

quote_sp_end_notation = re.compile("""
\A
(?P<quote><<)|(?P<sp>\|\|<)
\Z
""", re.VERBOSE)

def parse_body(body):
    """
    parse <body> tag
    """
    text = body.text
    lines = text.split("\n")

    result = []
    buffer, content, status, depth = [], {}, status_flag["NORMAL"], 0

    for l in lines:
        if status & status_flag["IN_QUOTE"]:
            end = quote_sp_end_notation.search(l)
            if end and depth == 0:
                ret = convert_quote(buffer, content['site'])
                result.extend(ret.split('\n'))
                buffer, content, status = [], {}, status_flag["NORMAL"]
                continue
            elif end and depth > 0:
                depth -= 1
            elif quote_sp_start_notation.search(l):
                depth += 1
            buffer.append(l)

        elif status & status_flag["IN_SUPERPRE"]:
            end = quote_sp_end_notation.search(l)
            if end:
                ret = convert_super_pre(buffer, content['filetype'])
                result.extend(ret.split('\n'))
                buffer, content, status = [], {}, status_flag["NORMAL"]
                continue
            buffer.append(l)

        else:
            start = quote_sp_start_notation.search(l)
            if start:
                content = start.groupdict()
                if content['quote']:
                    status = status_flag["IN_QUOTE"]
                elif content['sp']:
                    status = status_flag["IN_SUPERPRE"]
            else:
                result.append(l)

    result = [ convert_inlines(l) for l in result ]
    return '\n'.join(result)


def convert_quote(block, site):
    """
    convert quote notation
    
    TODO: find better algorithm for indenting block correctly.
    In reST paragraph requies blanked new line, and as of now
    'adjusted' list and following for loop handles that.
    """
    quoted = []
    buffer = []
    in_nest = False
    content = {}
    for l in block:
        if not in_nest:
            start = quote_sp_start_notation.search(l)
            if start:
                content = start.groupdict()
                in_nest = True
            else:
                quoted.append(indent + l)
                quoted.append('')
        else:
            end = quote_sp_end_notation.search(l)
            if end:
                if content['quote']:
                    if content['site']:
                        link_notation = content['site']
                    else:
                        link_notation = ""
                    lines = convert_quote(buffer, link_notation)
                    # find better algorithm
                    adjusted = [indent + l for l in lines.split("\n")[:-1]
                                if len(l.strip()) > 0]
                    for l in adjusted:
                        quoted.append(l)
                        quoted.append('')

                elif content['sp']:
                    lines = convert_super_pre(buffer, content['filetype'])
                    quoted.extend([indent + l for l in lines.split("\n")])

                in_nest = False
                buffer = []
                content = {}
            else:
                buffer.append(l)

    if site:
        link = convert_link(site)
        quote_msg = "(sited from %s)" % link
        quoted.append(quote_msg)
    return '\n'.join(quoted) + '\n'


# super pre notatino
#  - http://goo.gl/Q2szA
#  - http://goo.gl/xtQWf
def convert_super_pre(block, filetype):
    """
    convert super pre notation into code-block directive
    """
    indented_block = [ indent + l for l in block ]
    directive = [".. code-block:: %s\n" % filetype_map.get(filetype, "none")]
    return "\n".join(directive + indented_block) + "\n"


"""
convert in-line notations
  - chapter/section notation (*, **, ***)
  - hyperlink notation ([http://...])
  - list notation (-..., +..., etc)
  - id notation (id:user:20120512, etc)
  - fotolive notation ([f:id:user:20120512094500:image], etc)
"""

def convert_inlines(line):
    line = convert_section(line)
    line = convert_chapter(line)

    line = convert_link(line)
    line = convert_list(line)
    line = convert_fotolife(line)
    line = convert_id(line)
    return line


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
\A(?P<notation>\*{2,3})\s*(?P<title>.*)
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
(?P<url>(https?|ftp)://[\w\-\#\?\+\^\:\.\*\.&$@!=/]+?)
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
            print((url, title))
            converted = " `%s`_ " % (url,)
        elif image:
            if url[-3] in image_extensions:
                converted = ""
        target = target.replace(notation, converted)
    return target

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


def command():
    from argparse import ArgumentParser

    prog = "hatena2rst"
    description = "Hatena diary XML to reST converter"
    parser = ArgumentParser(prog=prog, description=description)

    parser.add_argument("filename", type=str)
    args = parser.parse_args()

    main(args.filename)


if __name__ == '__main__':
    command()
