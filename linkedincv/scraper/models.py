from django.db import models
from django.contrib.auth.models import User


class UserProfileHtml(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.JSONField()


class UserCookie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cookie = models.TextField(unique=True, max_length=500)
    access_agree = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username}::{self.cookie}'
