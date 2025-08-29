from django.db import models


class Team(models.Model):
    """Группа внутри подразделения"""

    title = models.CharField(
        verbose_name="Название группы",
        help_text="Введите название группы",
        max_length=150,
    )
    description = models.TextField(
        verbose_name="Описание группы",
        help_text="Введите описание группы",
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
