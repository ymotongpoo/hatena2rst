# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import *

"""
convert_super_pre()
"""
def test_quote():
    block = ["spam", "egg", "ham"]
    converted_block = convert_quote(block, None)
    assert "   spam\n\n   egg\n\n   ham\n\n" == converted_block

def test_nested_quote():
    block = ["spam", ">>", "egg", "ham", "<<", "foo"]
    converted_block = convert_quote(block, None)
    assert "   spam\n\n      egg\n\n      ham\n\n   foo\n\n" == converted_block

def test_nested_super_pre():
    block = ["spam", ">|python|", "import sys",
             "print(sys.version)", "||<", "egg"]
    converted_block = convert_quote(block, None)
    assert ("   spam\n\n" +
            "   .. code-block:: python\n\n" + 
            "      import sys\n" +
            "      print(sys.version)\n\n" +
            "   egg\n\n") == converted_block

def test_super_pre():
    block = ["import sys", "print(sys.version)"]
    filetype = "python"
    converted_block = convert_super_pre(block, filetype)
    assert (".. code-block:: python\n" +
            "\n" +
            "   import sys\n" +
            "   print(sys.version)\n") == converted_block
    

"""
convert_chapter()
"""
def test_chapter_normal():
    chapter = convert_chapter("*1207008000*test")
    assert "======\n test \n======" == chapter

def test_chapter_multibyte():
    chapter = convert_chapter("*1207008000*テストタイトル")
    assert "================\n テストタイトル \n================" == chapter
    

"""
convert_section() and related functions
"""
def test_string_width():
    test_cases = ["hello", "こんにちは", "abcあいう"]
    results = [string_width(x) for x in test_cases]
    assert [5, 10, 9] == results

def test_section_normal():
    section = convert_section("**section")
    assert "section\n======="

def test_section_multibyte():
    section = convert_section("**節")
    assert "節\n=="

def test_subsection_normal():
    section = convert_section("***subsection")
    assert "subsection\n----------"

def test_subsection_multibyte():
    section = convert_section("***小節")
    assert "小節\n----"

def test_no_section():
    nosection = convert_section("こんにちは")
    assert "こんにちは" == nosection


"""
convert_link()
"""
def test_normal_link():
    link = convert_link("[http://www.example.com]")
    assert " `http://www.example.com`_ " == link

def test_link_with_title():
    link = convert_link("[http://www.example.com:title]")
    assert " `http://www.example.com`_ " == link

def test_link_with_title():
    link = convert_link("[http://www.example.com:title=test]")
    assert " `test <http://www.example.com>`_ " == link

def test_link_with_bookmark():
    link = convert_link("[http://www.example.com:bookmark]")
    assert " `http://www.example.com`_ " == link

def test_link_with_title_and_bookmark():
    link = convert_link("[http://www.example.com:title=test:bookmark]")
    assert " `test <http://www.example.com>`_ " == link
    
def test_link_with_multibyte_title():
    link = convert_link("[http://www.spam.com:title=テストタイトル:bookmark]")
    assert " `テストタイトル <http://www.spam.com>`_ " == link

def test_link_with_port():
    link = convert_link("[http://www.example.com:8080/?spam=egg&ham=spam]")
    assert " `http://www.example.com:8080/?spam=egg&ham=spam`_ " == link

def test_link_with_port_and_title():
    link = convert_link("[http://www.example.com:8080/?spam=egg:title=ほげ]")
    assert " `ほげ <http://www.example.com:8080/?spam=egg>`_ " == link

def test_link_in_sentence():
    link = convert_link("詳しくは[http://spam.com:title=ここ]を見て下さい")
    assert "詳しくは `ここ <http://spam.com>`_ を見て下さい" == link

def test_no_link():
    nolink = convert_link("ふるかわとおる")
    assert "ふるかわとおる" == nolink


"""
convert_list()
"""
def test_level_1_list():
    list = convert_list("-こんにちは")
    assert "* こんにちは" == list

def test_level_2_list():
    list = convert_list("--こんにちは")
    assert "   * こんにちは" == list

def test_level_3_list():
    list = convert_list("---こんにちは")
    assert "      * こんにちは" == list

def test_level_1_numbered_list():
    list = convert_list("+こんにちは")
    assert "#. こんにちは"

def test_level_2_numbered_list():
    list = convert_list("++こんにちは")
    assert "   #. こんにちは" == list

def test_level_3_numbered_list():
    list = convert_list("+++こんにちは")
    assert "      #. こんにちは" == list


"""
convert_id()
"""
def test_id():
    id = convert_id("id:ymotongpoo")
    assert "`id:ymotongpoo <http://d.hatena.ne.jp/ymotongpoo/>`_" == id

def test_did():
    id = convert_id("d:id:ymotongpoo")
    assert "`d:id:ymotongpoo <http://d.hatena.ne.jp/ymotongpoo/>`_" == id

def test_date():
    date = convert_id("id:ymotongpoo:20060401")
    assert ("`id:ymotongpoo:20060401 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401>`_") == date

def test_ddate():
    date = convert_id("d:id:ymotongpoo:20060401")
    assert ("`d:id:ymotongpoo:20060401 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401>`_") == date

def test_page():
    page = convert_id("id:ymotongpoo:20060401:1143899261")
    assert ("`id:ymotongpoo:20060401:1143899261 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401/1143899261>`_") == page

def test_dpage():
    page = convert_id("d:id:ymotongpoo:20060401:1143899261")
    assert ("`d:id:ymotongpoo:20060401:1143899261 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401/1143899261>`_") == page

def test_semipage():
    page = convert_id("id:ymotongpoo:20060401#1143899261")
    assert ("`id:ymotongpoo:20060401#1143899261 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401#1143899261>`_") == page

def test_dsemipage():
    page = convert_id("d:id:ymotongpoo:20060401#1143899261")
    assert ("`d:id:ymotongpoo:20060401#1143899261 " +
            "<http://d.hatena.ne.jp/ymotongpoo/20060401#1143899261>`_") == page

def test_archive():
    archive = convert_id("id:ymotongpoo:archive")
    assert ("`id:ymotongpoo:archive " +
            "<http://d.hatena.ne.jp/ymotongpoo/archive>`_") == archive

def test_darchive():
    archive = convert_id("d:id:ymotongpoo:archive")
    assert ("`d:id:ymotongpoo:archive " +
            "<http://d.hatena.ne.jp/ymotongpoo/archive>`_") == archive

def test_archive_month():
    archive = convert_id("id:ymotongpoo:archive:200604")
    assert ("`id:ymotongpoo:archive:200604 " +
            "<http://d.hatena.ne.jp/ymotongpoo/archive/200604>`_") == archive

def test_darchive_month():
    archive = convert_id("d:id:ymotongpoo:archive:200604")
    assert ("`d:id:ymotongpoo:archive:200604 " +
            "<http://d.hatena.ne.jp/ymotongpoo/archive/200604>`_") == archive

def test_about():
    about = convert_id("id:ymotongpoo:about")
    assert ("`id:ymotongpoo:about " +
            "<http://d.hatena.ne.jp/ymotongpoo/about>`_") == about

def test_dabout():
    about = convert_id("d:id:ymotongpoo:about")
    assert ("`d:id:ymotongpoo:about " +
            "<http://d.hatena.ne.jp/ymotongpoo/about>`_") == about


"""
convert_fotolife() and related functions
"""
def test_image_directive_no_options():
    image_url = "http://torufurukawa.com/images/bucho.jpg"
    option = {}
    directive = generate_image_directive(image_url, option)
    assert ".. image:: http://torufurukawa.com/images/bucho.jpg\n" == directive

def test_image_directive_with_options():
    image_url = "http://torufurukawa.com/images/bucho.jpg"
    option = {
        'width': '60',
        'height': '100',
        'align': 'left',
        'scale': None
        }
    directive = generate_image_directive(image_url, option)
    assert (".. image:: http://torufurukawa.com/images/bucho.jpg\n" +
            "   :width: 60\n" +
            "   :align: left\n" +
            "   :height: 100\n") == directive


def test_image_option():
    option = 'w60,h100,right'
    option_dict = get_image_option(option)
    assert {'height': '100',
            'width': '60',
            'align': 'right',
            'scale': None} == option_dict

def test_image_option_2():
    option = 'small,left,w40,h10000'
    option_dict = get_image_option(option)
    assert {'height': '10000',
            'width': '40',
            'align': 'left',
            'scale': '20%'} == option_dict


def test_fotolife_normal():
    directive = convert_fotolife("[f:id:hatenadiary:20041007101545j:image]")
    assert (".. image:: http://f.hatena.ne.jp/images/fotolife/h/" +
            "hatenadiary/20041007/20041007101545j.png\n") == directive

def test_fotolife_with_option():
    directive = convert_fotolife("[f:id:hatenadiary:20041007101545j:image:w60,h100]")
    assert (".. image:: http://f.hatena.ne.jp/images/fotolife/h/" +
            "hatenadiary/20041007/20041007101545j.png\n" +
            "   :width: 60\n" +
            "   :height: 100\n") == directive

def test_fotolife_simple_user_link():
    link = convert_fotolife("[f:id:hatenadiary]")
    assert "`http://f.hatena.ne.jp/hatenadiary`_" == link

def test_fotolife_simple_pic_link():
    link = convert_fotolife("[f:id:hatenadiary:20041007101545j]")
    assert "`http://f.hatena.ne.jp/hatenadiary/20041007/20041007101545j`_" == link
