from django.db import models

from core.apps.common.models import TimeBaseModel


class HelpCategory(TimeBaseModel):
    """Категория справочной системы"""
    title = models.CharField(
        verbose_name="Название категории",
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name="URL-адрес",
        unique=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
    )
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )
    is_active = models.BooleanField(
        verbose_name="Активна",
        default=True,
    )

    class Meta:
        verbose_name = "Категория справки"
        verbose_name_plural = "Категории справки"
        db_table = "help_category"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
