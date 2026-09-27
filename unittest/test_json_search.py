"""Functional and security tests for recursive JSON search."""

import unittest

from policy import POLICY
from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    """Verify baseline behavior and explicit-role permissions."""

    def test_search_found(self):
        """Find the baseline summary and preserve all recursive matches."""
        summary = data["enrichmentInfo"]["issueDetails"]["issue"][0][key1]
        self.assertEqual(json_search(key1, data), [{key1: summary}])

        nested = {
            "match": 0,
            "items": [{"match": False}, [{"match": None}, {"match": ""}]],
            "tail": {"match": {"match": "inner"}},
        }
        self.assertEqual(
            json_search("match", nested),
            [
                {"match": 0},
                {"match": False},
                {"match": None},
                {"match": ""},
                {"match": {"match": "inner"}},
                {"match": "inner"},
            ],
        )

    def test_search_not_found(self):
        """Return an empty list for absent keys and scalar inputs."""
        self.assertEqual(json_search(key2, data), [])
        for value in ({}, [], None, 42, "issueSummary", True):
            with self.subTest(value=value):
                self.assertEqual(json_search(key1, value), [])

    def test_is_a_list(self):
        """Return lists for found, absent, and denied searches."""
        for key, role in (
            (key1, None),
            (key2, None),
            ("apiKey", "viewer"),
        ):
            with self.subTest(key=key, role=role):
                self.assertIsInstance(
                    json_search(key, data, role=role), list
                )
        self.assertEqual(
            json_search("items", {"items": [1, 2]}),
            [{"items": [1, 2]}],
        )

    def test_api_key_permissions(self):
        """Allow API credentials only for explicit admin roles (SR1)."""
        device = data["enrichmentInfo"]["connectedDevice"][0]["deviceDetails"]
        for role in ("admin", "operator", "viewer"):
            with self.subTest(role=role):
                expected = [{"apiKey": device["apiKey"]}] if role == "admin" else []
                self.assertEqual(
                    json_search("apiKey", data, role=role), expected
                )

    def test_management_ip_permissions(self):
        """Allow management IPs for admins and operators (SR2)."""
        device = data["enrichmentInfo"]["connectedDevice"][0]["deviceDetails"]
        for role in ("admin", "operator", "viewer"):
            with self.subTest(role=role):
                expected = (
                    [{"managementIpAddress": device["managementIpAddress"]}]
                    if role in ("admin", "operator")
                    else []
                )
                self.assertEqual(
                    json_search("managementIpAddress", data, role=role),
                    expected,
                )

    def test_issue_summary_permissions(self):
        """Allow summaries for all three defined roles (SR3)."""
        summary = data["enrichmentInfo"]["issueDetails"]["issue"][0][key1]
        for role in ("admin", "operator", "viewer"):
            with self.subTest(role=role):
                self.assertEqual(
                    json_search(key1, data, role=role), [{key1: summary}]
                )

    def test_unknown_roles_denied(self):
        """Deny unknown, empty, and mis-cased explicit roles (SR4)."""
        for key in POLICY:
            for role in ("guest", "", "Admin"):
                with self.subTest(key=key, role=role):
                    self.assertEqual(
                        json_search(key, data, role=role), []
                    )

    def test_nested_policy_permissions(self):
        """Enforce policy throughout nested dictionaries and lists (SR5-6)."""
        for key, allowed_roles in POLICY.items():
            nested = [
                {key: "first"},
                {"wrapper": [[{key: "second"}], {"deep": {key: "third"}}]},
            ]
            for role in ("admin", "operator", "viewer", "guest"):
                with self.subTest(key=key, role=role):
                    expected = (
                        [{key: "first"}, {key: "second"}, {key: "third"}]
                        if role in allowed_roles
                        else []
                    )
                    self.assertEqual(
                        json_search(key, nested, role=role), expected
                    )

    def test_no_role_backward_compatibility(self):
        """Preserve unrestricted searches for omitted or None roles."""
        for key in POLICY:
            nested = [{key: "first"}, {"nested": [{key: "second"}]}]
            with self.subTest(key=key):
                self.assertEqual(json_search(key, nested), [{key: "first"}, {key: "second"}])
                self.assertEqual(
                    json_search(key, nested, role=None),
                    [{key: "first"}, {key: "second"}],
                )


if __name__ == "__main__":
    unittest.main()
