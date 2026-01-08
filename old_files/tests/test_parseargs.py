#!/usr/bin/env python3
import sys

import pytest

from src.classes.parseargs import ParseArgs


class TestParseArgs():
    def setUp(self):
        pass

    def tearDown(self):
        del sys.argv[1:]

    def test_print_help(self):
        args = []
        myparser = ParseArgs(args)
        assert len(myparser.args) == 0

    def test_print_version(self):
        self.setUp()
        sys.argv.append('--version')
        with pytest.raises(SystemExit):
            myparser = ParseArgs(sys.argv[1:])
            assert myparser.action == 'version'
            assert len(myparser.args) == 1
        self.tearDown()

    def test_get_action(self):
        self.setUp()
        myparser = ParseArgs(sys.argv[1:])
        assert myparser.action == ''
        self.tearDown()

    def test_test_argument(self):
        self.setUp()
        sys.argv.append('--test')
        myparser = ParseArgs(sys.argv)
        assert myparser.action == 'test'
        self.tearDown()
