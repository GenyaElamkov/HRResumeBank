from django.conf import settings
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
    created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Кто создал шаблон",
        on_delete=models.SET_NULL,
        null=True,
        related_name="templates",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Шаблон резюме/карточка"
        verbose_name_plural = "Шаблоны резюме/карточки"
        db_table = "template"
