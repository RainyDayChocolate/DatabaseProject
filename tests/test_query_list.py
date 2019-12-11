#!/usr/bin/env python3

import unittest
from client_query_manager.query_list import Query_list

class query_list_testCases(unittest.TestCase):
    def setUp(self):
        self.queryL = Query_list()
    
    def test_create_USFlightDelay_set(self):
        self.queryL.create_USFlightDelay_set()

    def test_create_USAccidents_set(self):
        self.queryL.create_USAccidents_set()

    def test_create_USGunViolence_set(self):
        self.queryL.create_USGunViolence_set()

if __name__=='__main__':
    unittest.main()