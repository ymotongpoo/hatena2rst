# -*- coding: utf-8 -*-

codec = "utf-8"
indent = "   "
max_depth = 3
image_extensions = ['png', 'PNG, ''jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF']

status_flag = {
    "NORMAL":         1 << 0,
    "IN_QUOTE":       1 << 1,
    "IN_SUPERPRE":    1 << 2,
}

"""
lexer mapping between hatena and pygments
  - hatena supre pre: http://goo.gl/xtQWf
  - pygments: http://goo.gl/tt8cl

  mapping rule is "super pre" -> "pygments"
"""
filetype_map = {
    "antlr": "antlr",
    "actionscript": "actionscript3",
    "c": "c",
    "cmake": "cmake",
    "cs": "c#",
    "cl": "common-lisp",
    "cpp": "cpp",
    "css": "css",
    "d": "d",
    "django": "jinja",
    "erlang": "erlang",
    "fortran": "fortran",
    "go": "go",
    "groovy": "groovy",
    "haskell": "haskell",
    "html": "html",
    "java": "java",
    "javascript": "javascript",
    "matlab": "matlab",
    "objc": "objective-c",
    "ocaml": "ocaml",
    "perl": "perl",
    "php": "php",
    "python": "python",
    "ruby": "ruby",
    "scala": "scala",
    "scheme": "scheme",
    "sh": "bash",
    "sql": "sql",
    "tcsh": "tcsh",
    "tex": "tex",
    "xml": "xml",
    "yaml": "yaml",
}
