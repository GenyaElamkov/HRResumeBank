from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель User"""
    surname = models.CharField(
        verbose_name="Отчество",
        max_length=150,
        blank=True,
        null=True,
    )
