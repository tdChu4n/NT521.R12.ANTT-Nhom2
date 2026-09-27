import unittest
from recursive_json_search import json_search
from test_data import data,key1,key2

class json_search_test(unittest.TestCase):
    """test module to test search function in recursive_json_search.py"""

    def test_search_found(self):
        """key should be found, return list should not be empty"""
        self.assertTrue([] != json_search(key1,data))

    def test_search_not_found(self):
        """key should not be found, should return an empty list"""
        self.assertEqual([],json_search(key2,data))

    def test_is_a_list(self):
        """Should return a list"""
        self.assertIsInstance(json_search(key1,data),list)

    def test_api_key_is_limited_to_admin(self):
        """Only admin may retrieve apiKey"""
        self.assertNotEqual([],json_search("apiKey",data,role="admin"))
        self.assertEqual([],json_search("apiKey",data,role="operator"))
        self.assertEqual([],json_search("apiKey",data,role="viewer"))

    def test_management_ip_allows_operator_but_not_viewer(self):
        """Admin and operator may retrieve managementIpAddress"""
        self.assertNotEqual([],json_search("managementIpAddress",data,role="admin"))
        self.assertNotEqual([],json_search("managementIpAddress",data,role="operator"))
        self.assertEqual([],json_search("managementIpAddress",data,role="viewer"))

    def test_issue_summary_allows_each_configured_role(self):
        """All configured roles may retrieve issueSummary"""
        for role in ("admin","operator","viewer"):
            self.assertNotEqual([],json_search("issueSummary",data,role=role))

if __name__ == '__main__':
    unittest.main()
