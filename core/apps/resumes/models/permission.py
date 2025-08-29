from django.db import models


class Permission(models.Model):
    """Разрешение"""

    title = models.CharField(
        verbose_name="Названия действия",
        help_text="Введите действия",
        max_length=100,
    )
    code = models.CharField(
        verbose_name="Уникальный код разрешения",
        help_text="Введите код разрешения",
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание назначения решения",
        help_text="Ввидите описание",
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Разрешение"
        verbose_name_plural = "Разрешении"
