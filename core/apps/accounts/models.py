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

    def get_full_name(self):
        full_name = super().get_full_name()
        if self.surname:
            full_name = f"{full_name} {self.surname}" if full_name else self.surname
        return full_name or self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "custom_user"
