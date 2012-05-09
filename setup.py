# -*- coding: utf-8 -*-

import sys
import os.path
try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

def read_file(name):
    path = os.path.join(os.path.dirname(__file__), name)
    f = open(os.path.abspath(path), 'r')
    data = f.read()
    f.close()
    return data

short_description = "Hatena archive XML converter into reST"

try:
    long_description = read_file('README.rst'),
except IOError:
    long_description = ""

version = '0.0.1'

classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Topic :: Software Development :: Libraries',
    'Topic :: Text Processing :: Markup :: XML',
    'Topic :: Utilities',
    ]

install_requires=[
	'distribute',
	'lxml>=2.3'
	]
if sys.version_info[0:2] == (2, 6):
    install_requires.append('argparse')

setup(
    name="hatena2rst",
    version=version,
    url=r"https://github.com/ymotongpoo/hatena2rst",
    license='New BSD',
    author="Yoshifumi YAMAGUCHI",
    author_email="ymotongpoo at gmall.com",
    description=short_description,
    long_description=long_description,
    install_requires=install_requires,
    packages=['hatena2rst'],
    package_data={},
    entry_points=dict(
        console_scripts=["hatena2rst = main:main"]
        ),
    extras_require = dict(
        test=[
            'pytest>=2.2',
            'coverage>=3.5',
            'mock>=0.8.0'
            ]
        ),
    test_suite='test.suite',
    tests_require=['pytest']
    )

