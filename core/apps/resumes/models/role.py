from django.db import models


class Role(models.Model):
    """Роль"""
    title = models.CharField(
        verbose_name="Название роли",
        help_text="Введите название роли",
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание роли",
        help_text="Введите описание роли",
        blank=True,
    )

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"