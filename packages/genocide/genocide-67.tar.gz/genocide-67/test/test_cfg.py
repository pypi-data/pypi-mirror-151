# This file is placed in the Public Domain.


"configuration tests"


import os
import sys


import unittest


from genocide.evt import Event
from genocide.obj import Object, edit, update


class Config(Object):

    pass


class Test_Config(unittest.TestCase):

    def test_parse(self):
        e = Event()
        e.parse("cfg mod=irc")
        self.assertEqual(e.sets.mod, "irc")

    def test_edit(self):
        e = Event()
        o = Object()
        update(o, {"mod": "irc,rss"})
        edit(e, o)
        self.assertEqual(e.mod, "irc,rss")
