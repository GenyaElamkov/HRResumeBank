from django.db import models
from django.contrib.auth.models import User

from core.apps.common.models import TimeBaseModel
from core.apps.resumes.models.template import Template


class Entity(TimeBaseModel):
    """Запись резюме/Сущность"""

    template = models.ForeignKey(
        Template,
        verbose_name="Шаблон",
        on_delete=models.CASCADE,
        related_name="entity_template",
    )
    created = models.ForeignKey(
        User,
        verbose_name="Кто создал запись",
        on_delete=models.CASCADE,
        related_name="created_template"
    )

    def __str__(self):
        return f"{self.template}: {self.created}"

    class Meta:
        verbose_name = "Запись резюме/Сущность"
        verbose_name_plural = "Записи резюме/Сущности"