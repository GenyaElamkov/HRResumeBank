from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.cache import cache
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
        on_delete=models.PROTECT,
        related_name="created_card",
    )
    values = models.JSONField(
        verbose_name="Значения полей",
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

    def save(self, *args, **kwargs):
        # Cache clearing
        cache_key = f"card_{self.id}_status_color"
        cache.delete(cache_key)
        super().save(*args, **kwargs)

    def get_status_color(self) -> str:
        """Получить цвет статуса карточки"""
        color_map = {
            'кандидат': 'linear-gradient(to right, var(--success-dark), var(--success))',
            'уволен': 'linear-gradient(to right, var(--danger-dark), var(--danger))',
            'default': 'linear-gradient(to right, var(--primary), var(--secondary))',
        }

        cache_key = f"card_{self.id}_status_color"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        status_keys = {'статус', 'status', 'state', 'состояние'}
        value_lower = next(
            (
                str(v).lower() for k, v in self.values.items()
                if k.lower() in status_keys and isinstance(v, (str, int))
            ),
            None,
        )

        color = color_map.get(value_lower, color_map['default'])
        cache.set(cache_key, color, 300)
        return color

    def __str__(self):
        return f"{self.template.title} Карточка #{self.id}"

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        db_table = "card"
        ordering = ['-create_at']
        indexes = [
            GinIndex(fields=["values"]),
        ]
