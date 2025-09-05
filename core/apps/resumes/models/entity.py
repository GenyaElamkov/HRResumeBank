from django.conf import settings
from django.db import models

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
        settings.AUTH_USER_MODEL,
        verbose_name="Кто создал запись",
        on_delete=models.CASCADE,
        related_name="created_template",
    )
    main_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.main_name or f"Entity #{self.id}"

    class Meta:
        verbose_name = "Запись резюме/Сущность"
        verbose_name_plural = "Записи резюме/Сущности"
