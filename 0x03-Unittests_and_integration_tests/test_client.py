#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
import fixtures  # ALX fixtures.py


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct org data"""
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)

        self.assertEqual(client.org, {"name": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch.object(GithubOrgClient, "org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url uses org['repos_url']"""
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }

        client = GithubOrgClient("test-org")
        result = client._public_repos_url

        self.assertEqual(
            result, "https://api.github.com/orgs/test-org/repos"
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos behavior"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test-org/repos"
        ) as mock_url:

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            expected = ["repo1", "repo2"]
            self.assertEqual(result, expected)

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": fixtures.fixture["org_payload"],
        "repos_payload": fixtures.fixture["repos_payload"],
        "expected_repos": fixtures.fixture["expected_repos"],
        "apache2_repos": fixtures.fixture["apache2_repos"]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level patching for requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Side effect to return correct fixture based on URL
        def get_json_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url.endswith("/orgs/test-org"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/orgs/test-org/repos"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repository names from the fixture"""
        self.get_patcher = self.__class__.get_patcher  
        client = GithubOrgClient("test-org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos with license='apache-2.0'"""
        self.get_patcher = self.__class__.get_patcher  
        client = GithubOrgClient("test-org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
