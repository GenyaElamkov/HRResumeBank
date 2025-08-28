from django.db import models


class Department(models.Model):
    """Подразделение"""
    title = models.CharField(
        verbose_name="Название подразделения",
        help_text="Введите подразделение",
        max_length=150,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Родительское подразделение",
        help_text="Выберите подразделение",
        related_name="children",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание",
        blank=True,
    )

    class Meta:
        verbose_name = "Поздразделение"
        verbose_name_plural = "Подразделение"

    def __str__(self):
        return self.title
