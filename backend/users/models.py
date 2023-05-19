from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователей."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail пользователя')
    # password = models.CharField(max_length=100)
    # auth_token = Token()