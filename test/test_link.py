# -*- coding: utf-8 -*-

from hatena2rst import convert_link

def test_normal_link():
    test_notation = "[http://www.example.com:title=test]"
    link = convert_link(test_notation)
    assert "`test <http://www.example.com>`_" == link
    
