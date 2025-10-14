from django.db import models

from core.apps.common.models import TimeBaseModel


class HelpArticle(TimeBaseModel):
    """Статья справочной системы"""
    title = models.CharField(
        verbose_name="Заголовок",
        max_length=300,
    )
    slug = models.SlugField(
        verbose_name="URL-адрес",
        unique=True,
    )
    content = models.TextField(
        verbose_name="Содержание",
    )
    short_description = models.TextField(
        verbose_name="Краткое описание",
        blank=True,
    )
    category = models.ForeignKey(
        to="help.HelpCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name='articles',
    )
    tags = models.CharField(
        verbose_name="Теги",
        max_length=500,
        blank=True,
        help_text="Разделяйте теги запятыми",
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )
    is_featured = models.BooleanField(
        verbose_name="Популярная статья",
        default=False,
    )
    view_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        default=0,
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )
    related_template = models.ForeignKey(
        'resumes.Template',
        verbose_name="Связанный шаблон",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Статья справки"
        verbose_name_plural = "Статьи справки"
        db_table = "help_article"
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['is_published', 'category']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title
