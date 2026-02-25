from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from .models import GitHubAppIntegration
from .services.github_app_service import (fetch_repositories , fetch_commits , fetch_all_commits)


def github_app_install(request):
    return redirect(
        "https://github.com/apps/tool-integration/installations/new"
    )


def github_app_callback(request):
    installation_id = request.GET.get("installation_id")
    customer_id = "company_123"  # Make dynamic later

    GitHubAppIntegration.objects.update_or_create(
        customer_id=customer_id,
        defaults={"installation_id": installation_id},
    )

    return JsonResponse({"message": "GitHub App connected successfully"})


def get_customer_repos(request, customer_id):
    integration = GitHubAppIntegration.objects.get(
        customer_id=customer_id
    )

    data = fetch_repositories(integration.installation_id)
    return JsonResponse(data, safe=False)

def get_repo_commits(request, customer_id, repo_name):
    integration = GitHubAppIntegration.objects.get(
        customer_id=customer_id
    )

    # First fetch repositories
    repos = fetch_repositories(integration.installation_id)

    # Find matching repo
    repo = next(
        (r for r in repos if r["name"] == repo_name),
        None
    )

    if not repo:
        return JsonResponse({"error": "Repository not found"}, status=404)

    owner = repo["owner"]

    data = fetch_commits(
        integration.installation_id,
        owner,
        repo_name
    )

    return JsonResponse(data, safe=False)


def get_all_commits(request, customer_id):
    integration = GitHubAppIntegration.objects.get(
        customer_id=customer_id
    )

    data = fetch_all_commits(integration.installation_id)

    return JsonResponse(data, safe=False)