from django.conf import settings
from django.db import models


class Log(models.Model):
    """Журнал действий"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Кто выполнил действие",
        on_delete=models.SET_NULL,
        related_name="logs",
        null=True,
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

    def __str__(self):
        return f"{self.user}: {self.action}"

    class Meta:
        verbose_name = "Журнал действий"
        verbose_name_plural = "Жарнал действий"
        db_table = "log"
