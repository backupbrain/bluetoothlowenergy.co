#!/usr/bin/python

import sys
import inspect
from os import path
import base64
import json
import unittest

class DatabaseObjectTestCase(unittest.TestCase):

    ''' test str2bool '''

    def test_underscore_oneword(self):
        name = "Object"
        expected_name = 'object'

        resulting_name = DatabaseObject.camel_to_underscore(name)

        self.assertEquals(expected_name, resulting_name)


    def test_underscore_twowords(self):
        name = "ObjectName"
        expected_name = 'object_name'

        resulting_name = DatabaseObject.camel_to_underscore(name)

        self.assertEquals(expected_name, resulting_name)




if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        currentdir = path.dirname(path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = path.dirname(currentdir)
        sys.path.insert(0,parentdir) 
        from DatabaseObject import DatabaseObject
    else:
        from ..DatabaseObject import DatabaseObject

    unittest.main()
