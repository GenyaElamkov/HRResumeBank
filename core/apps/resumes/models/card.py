from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from core.apps.common.models import TimeBaseModel


class Card(TimeBaseModel):
    """Карточка"""

    template = models.ForeignKey(
        to="resumes.Template",
        verbose_name="Шаблон",
        on_delete=models.CASCADE,
        related_name="cards",
    )
    created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Кто создал запись",
        on_delete=models.CASCADE,
        related_name="created_template",
    )
    values = models.JSONField(
        encoder=DjangoJSONEncoder,
        default=dict,
    )
    main_name = models.CharField(
        verbose_name="Наименование карточки",
        max_length=255,
        blank=True,
        null=True,
        editable=False,
    )

    def __str__(self):
        return f"{self.template.title} Карточка #{self.id}"

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        db_table = "card"

        indexes = [
            GinIndex(fields=["values"]),
        ]
