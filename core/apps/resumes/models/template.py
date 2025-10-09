from django.db import models

from core.apps.common.models import TimeBaseModel


class Template(TimeBaseModel):
    """Шаблон резюме/карточка"""

    title = models.CharField(
        verbose_name="Название шаблона",
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"
        db_table = "template"
