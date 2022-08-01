from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    """Override system user."""

    role = models.CharField(max_length=255, null=True, blank=True, choices=(
        ('admin', 'admin'),
        ('normal', 'normal')
    ))

    objects = UserManager()

    # to check if user is replicated to keycloak or not
    is_created_in_keycloak = models.BooleanField()

    def __str__(self):
        return f'Email: {self.username} and Role: {self.role}'
