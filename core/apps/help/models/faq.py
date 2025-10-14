from django.db import models

from core.apps.common.models import TimeBaseModel


class FAQ(TimeBaseModel):
    """Часто задаваемые вопросы"""
    question = models.CharField(
        verbose_name="Вопрос",
        max_length=500,
    )
    answer = models.TextField(
        verbose_name="Ответ",
    )
    category = models.ForeignKey(
        to="help.HelpCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name='faqs',
    )
    is_published = models.BooleanField(
        verbose_name="Опубликовано",
        default=True,
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядок",
        default=0,
    )

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"
        db_table = "help_faq"
        ordering = ['order', 'question']
