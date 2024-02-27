from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class ExportedCv(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    basic_information = models.JSONField()
    education = models.JSONField()
    experiences = models.JSONField()
    licenses = models.JSONField()
    projects = models.JSONField()
    hide_basic_information_items = models.JSONField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_export'
            )
        ]
