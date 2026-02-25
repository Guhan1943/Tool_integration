import jwt
import time
import requests
import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

BASE_URL = "https://api.github.com"


def generate_app_jwt():
    """
    Generates a JWT for authenticating as a GitHub App.
    """

    private_key_path = settings.GITHUB_APP_PRIVATE_KEY_PATH

    if not os.path.exists(private_key_path):
        raise ImproperlyConfigured(
            f"GitHub private key not found at: {private_key_path}"
        )

    with open(private_key_path, "r") as f:
        private_key = f.read()

    payload = {
        "iat": int(time.time()) - 60,   # allow 1 min clock drift
        "exp": int(time.time()) + 540,  # 9 minutes max (safe under 10)
        "iss": str(settings.GITHUB_APP_ID),
    }

    encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256")

    print("JWT:", encoded_jwt)
    print("JWT parts:", encoded_jwt.count("."))

    return encoded_jwt


def get_installation_token(installation_id):
    """
    Exchanges GitHub App JWT for installation access token.
    """

    jwt_token = generate_app_jwt()

    url = f"{BASE_URL}/app/installations/{installation_id}/access_tokens"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        },
    )

    if response.status_code != 201:
        raise Exception(
            f"Failed to get installation token: {response.status_code} {response.text}"
        )

    return response.json().get("token")

def fetch_repositories(installation_id):
    token = get_installation_token(installation_id)

    response = requests.get(
        f"{BASE_URL}/installation/repositories",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )

    repos = response.json().get("repositories", [])

    return [
        {
            "name": repo.get("name"),
            "owner": repo.get("owner", {}).get("login"),
            "private": repo.get("private"),
            "default_branch": repo.get("default_branch"),
        }
        for repo in repos
    ]

def fetch_commits(installation_id, owner, repo_name):
    token = get_installation_token(installation_id)

    response = requests.get(
        f"{BASE_URL}/repos/{owner}/{repo_name}/commits",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch commits: {response.status_code} {response.text}"
        )

    commits = response.json()

    return [
        {
            "sha": commit.get("sha"),
            "author": commit.get("commit", {}).get("author", {}).get("name"),
            "message": commit.get("commit", {}).get("message"),
            "date": commit.get("commit", {}).get("author", {}).get("date"),
        }
        for commit in commits
    ]


def fetch_all_commits(installation_id):
    token = get_installation_token(installation_id)

    # Get all repositories
    repos_response = requests.get(
        f"{BASE_URL}/installation/repositories",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )

    if repos_response.status_code != 200:
        raise Exception(
            f"Failed to fetch repositories: {repos_response.status_code} {repos_response.text}"
        )

    repos = repos_response.json().get("repositories", [])

    all_commits = []

    for repo in repos:
        owner = repo.get("owner", {}).get("login")
        repo_name = repo.get("name")

        commits_response = requests.get(
            f"{BASE_URL}/repos/{owner}/{repo_name}/commits",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
        )

        if commits_response.status_code == 200:
            commits = commits_response.json()

            for commit in commits:
                all_commits.append({
                    "repo": repo_name,
                    "owner": owner,
                    "sha": commit.get("sha"),
                    "author": commit.get("commit", {}).get("author", {}).get("name"),
                    "message": commit.get("commit", {}).get("message"),
                    "date": commit.get("commit", {}).get("author", {}).get("date"),
                })

    return all_commits