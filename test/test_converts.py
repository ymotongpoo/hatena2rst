# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import convert_link

def check_correspondency(origin, target):
    def function(origin, target):
    link = convert_link(origin)
    assert target == link


"""
convert_link()
"""
def test_normal_link():
    check_correspondency("[http://www.example.com]",
                         "`http://www.example.com`_")

def test_link_with_title():
    check_correspondency("[http://www.example.com:title]",
                         "`http://www.example.com`_")

def test_link_with_title():
    check_correspondency("[http://www.example.com:title=test]",
                         "`test <http://www.example.com>`_")

def test_link_with_bookmark():
    check_correspondency("[http://www.example.com:bookmark]",
                         "`http://www.example.com`_")

def test_link_with_title_and_bookmark():
    check_correspondency("[http://www.example.com:title=test:bookmark]",
                         "`test <http://www.example.com>`_")
    
def test_link_with_multibyte_title():
    check_correspondency("[http://www.spam.com:title=テストタイトル:bookmark]",
                         "`テストタイトル <http://www.spam.com>`_")

def test_link_with_port():
    check_correspondency("[http://www.example.com:8080/?spam=egg&ham=spam]",
                         "`http://www.example.com:8080/?spam=egg&ham=spam`_")


"""
convert_list()
"""
def test_level_1_list():
    check_correspondency("-こんにちは",
                         "- こんにちは")

def test_level_2_link():
    check_correspondency("--こんにちは",
                         "   * こんにちは")

def test_level_3_link():
    check_correspondency("---こんにちは",
                         "      - こんにちは")
