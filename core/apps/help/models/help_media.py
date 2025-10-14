from django.db import models

from core.apps.common.models import TimeBaseModel


class HelpMedia(TimeBaseModel):
    """Медиафайлы для статей справки"""
    article = models.ForeignKey(
        to="help.HelpArticle",
        verbose_name="Статья",
        on_delete=models.CASCADE,
        related_name='media_files',
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to='help_system/images/',
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
    )
    caption = models.CharField(
        verbose_name="Подпись",
        max_length=300,
        blank=True,
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )

    class Meta:
        verbose_name = "Медиафайл справки"
        verbose_name_plural = "Медиафайлы справки"
        db_table = "help_media"
        ordering = ['order']
