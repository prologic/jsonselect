#!/usr/bin/env python


"""test.py -- Testing individual test cases

::
    
    python -i test.py conformance_tests/upstream/level_3/basic.json conformance_tests/upstream/level_3/basic_has.selector conformance_tests/upstream/level_3/basic_has.output
"""


from __future__ import print_function

import sys
from json import loads
from pprint import pprint  # noqa


from jsonselect.jsonselect import Parser


document_file = sys.argv[1]
selector_file = sys.argv[2]
expected_file = sys.argv[3]

document = loads(open(document_file, "r").read())
selector = open(selector_file, "r").read().strip()
expected = open(expected_file, "r").read().strip()

p = Parser(document)
x = p.parse(selector)
