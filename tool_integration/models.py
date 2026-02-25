from django.db import models

class GitHubAppIntegration(models.Model):
    customer_id = models.CharField(max_length=100, unique=True)
    installation_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_id