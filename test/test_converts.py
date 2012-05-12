# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import *

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
    assert "`http://www.example.com`_" == link

def test_link_with_title():
    link = convert_link("[http://www.example.com:title]")
    assert "`http://www.example.com`_" == link

def test_link_with_title():
    link = convert_link("[http://www.example.com:title=test]")
    assert "`test <http://www.example.com>`_" == link

def test_link_with_bookmark():
    link = convert_link("[http://www.example.com:bookmark]")
    assert "`http://www.example.com`_" == link

def test_link_with_title_and_bookmark():
    link = convert_link("[http://www.example.com:title=test:bookmark]")
    assert "`test <http://www.example.com>`_" == link
    
def test_link_with_multibyte_title():
    link = convert_link("[http://www.spam.com:title=テストタイトル:bookmark]")
    assert "`テストタイトル <http://www.spam.com>`_" == link

def test_link_with_port():
    link = convert_link("[http://www.example.com:8080/?spam=egg&ham=spam]")
    assert "`http://www.example.com:8080/?spam=egg&ham=spam`_" == link

def test_link_with_port_and_title():
    link = convert_link("[http://www.example.com:8080/?spam=egg:title=ほげ]")
    assert "`ほげ <http://www.example.com:8080/?spam=egg>`_" == link

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

def test_level_2_link():
    list = convert_list("--こんにちは")
    assert "   * こんにちは" == list

def test_level_3_link():
    list = convert_list("---こんにちは")
    assert "      * こんにちは" == list



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
