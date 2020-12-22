from django.db import models
from django.contrib.auth.models import AbstractUser


class Roles(models.Model):
    role_name = models.CharField(max_length=30)

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    user_type = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

