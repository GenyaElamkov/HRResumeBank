from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя Django с поддержкой отчества."""

    surname = models.CharField(
        verbose_name="Отчество",
        max_length=150,
        blank=True,
        null=True,
    )

    def get_full_name(self):
        """Формирует полное имя с отчеством."""
        full_name = super().get_full_name()
        parts = full_name.split(" ") if full_name else []
        if self.surname:
            parts.insert(1, self.surname)
        return ' '.join(parts) or self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = "custom_user"
        indexes = [models.Index(fields=['username']), models.Index(fields=['email'])]
