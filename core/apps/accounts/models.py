from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель User"""

    surname = models.CharField(
        verbose_name="Отчество",
        max_length=150,
        blank=True,
        null=True,
    )
