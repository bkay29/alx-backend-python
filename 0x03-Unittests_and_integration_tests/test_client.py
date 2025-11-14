#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct org data"""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)

        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch.object(GithubOrgClient, "org", new_callable=MagicMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url uses org['repos_url']"""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }

        client = GithubOrgClient("test-org")
        result = client._public_repos_url

        self.assertEqual(
            result,
            "https://api.github.com/orgs/test-org/repos"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos behavior"""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}},
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=MagicMock,
            return_value="https://api.github.com/orgs/test-org/repos"
        ) as mock_url:

            client = GithubOrgClient("test-org")

            # No license filter
            result = client.public_repos()
            self.assertEqual(
                result, ["repo1", "repo2", "repo3"]
            )

            # With license filter
            apache = client.public_repos(license="apache-2.0")
            self.assertEqual(apache, ["repo1", "repo3"])

        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test-org/repos"
        )


if __name__ == "__main__":
    unittest.main()