from django.db import models
from django.contrib.auth.models import User


class Log(models.Model):
    """Журнал действий"""

    user = models.ForeignKey(
        User,
        verbose_name="Кто выполнил действие",
        on_delete=models.SET_NULL,
        related_name="logs",
        null=True
    )
    action = models.CharField(
        verbose_name="Тип действия",
        max_length=100,
    )
    details = models.TextField(
        verbose_name="Дополнительные детали",
        blank=True,
        null=True,
    )
    timestamp = models.DateTimeField(
        verbose_name="Время события",
        auto_now_add=True,
    )