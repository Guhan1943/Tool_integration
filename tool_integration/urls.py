from django import views
from django.urls import path
from .views import (
    github_app_install,
    github_app_callback,
    get_customer_repos,
    get_repo_commits,
    get_all_commits,
)

urlpatterns = [
    path("github/app/install/", github_app_install),
    path("github/app/callback/", github_app_callback),
    path("repos/<str:customer_id>/", get_customer_repos),
    path("commits/<str:customer_id>/<str:repo_name>/",get_repo_commits),
    path(
    "all-commits/<str:customer_id>/",
    get_all_commits,
),
    
]