# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import convert_link, convert_list, convert_section

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
convert_section()
"""
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

