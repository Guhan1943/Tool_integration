import jwt
import time
import requests
from django.conf import settings

BASE_URL = "https://api.github.com"


def generate_app_jwt():
    with open(settings.GITHUB_APP_PRIVATE_KEY_PATH, "r") as f:
        private_key = f.read()

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "iss": settings.GITHUB_APP_ID,
    }

    return jwt.encode(payload, private_key, algorithm="RS256")

def get_installation_token(installation_id):
    jwt_token = generate_app_jwt()

    url = f"{BASE_URL}/app/installations/{installation_id}/access_tokens"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        },
    )

    return response.json().get("token")

def fetch_repositories(installation_id):
    token = get_installation_token(installation_id)

    response = requests.get(
        f"{BASE_URL}/installation/repositories",
        headers={"Authorization": f"Bearer {token}"},
    )

    repos = response.json().get("repositories", [])

    return [
        {
            "name": repo["name"],
            "private": repo["private"],
            "default_branch": repo["default_branch"],
        }
        for repo in repos
    ]