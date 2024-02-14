from django.db import models


class UserProfileHtml(models.Model):
    cookie = models.TextField(unique=True, max_length=500)
    user = models.TextField(max_length=255)
    data = models.JSONField()
