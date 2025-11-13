#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        result = client.org()
        self.assertEqual(result, {"name": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from org"""
        fake_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        client = GithubOrgClient("test-org")
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = fake_payload
            result = client._public_repos_url

        self.assertEqual(result, fake_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()

