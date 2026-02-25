from django.urls import path
from .views import (
    github_app_install,
    github_app_callback,
    get_customer_repos,
)

urlpatterns = [
    path("github/app/install/", github_app_install),
    path("github/app/callback/", github_app_callback),
    path("repos/<str:customer_id>/", get_customer_repos),
]