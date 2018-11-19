import unittest
import os
from RasaHost import host
from RasaHost.services.query_parser import QueryParser

class QueryParserTests(unittest.TestCase):
    
    def test_parser(self):
        parser = QueryParser()

        result = parser.parse("request:123")
        self.assertEqual([{"request":"123"}], result)

        result = parser.parse("request:123 bla")
        self.assertEqual([{"request":"123"}, "bla"], result)

