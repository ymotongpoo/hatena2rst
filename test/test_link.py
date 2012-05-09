# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from hatena2rst import convert_link

def test_normal_link():
    test_notation = "[http://www.example.com]"
    link = convert_link(test_notation)
    assert "`http://www.example.com`_" == link

def test_link_with_title():
    test_notation = "[http://www.example.com:title]"
    link = convert_link(test_notation)
    assert "`http://www.example.com`_" == link

def test_link_with_title():
    test_notation = "[http://www.example.com:title=test]"
    link = convert_link(test_notation)
    assert "`test <http://www.example.com>`_" == link

def test_link_with_bookmark():
    test_notation = "[http://www.example.com:bookmark]"
    link = convert_link(test_notation)
    assert "`http://www.example.com`_" == link

def test_link_with_title_and_bookmark():
    test_notation = "[http://www.example.com:title=test:bookmark]"
    link = convert_link(test_notation)
    assert "`test <http://www.example.com>`_" == link
    

