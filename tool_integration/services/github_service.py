import requests

BASE_URL = "https://api.github.com"


def get_repositories(access_token):
    url = f"{BASE_URL}/user/repos?per_page=100"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10
    )

    if response.status_code != 200:
        return {"error": "Failed to fetch repositories"}

    repos = response.json()

    return [
        {
            "name": repo["name"],
            "private": repo["private"],
            "default_branch": repo["default_branch"],
            "updated_at": repo["updated_at"],
        }
        for repo in repos
    ]


def get_branch_protection(access_token, owner, repo, branch):
    url = f"{BASE_URL}/repos/{owner}/{repo}/branches/{branch}/protection"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10
    )

    if response.status_code == 200:
        return {"branch_protected": True}
    elif response.status_code == 404:
        return {"branch_protected": False}
    else:
        return {"error": "Unable to check protection"}


def get_org_info(access_token):
    url = f"{BASE_URL}/user/orgs"

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10
    )

    if response.status_code != 200:
        return {"error": "Failed to fetch organizations"}

    return [{"org_name": org["login"]} for org in response.json()]