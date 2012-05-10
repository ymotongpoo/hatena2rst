# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import convert_link, convert_list

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
