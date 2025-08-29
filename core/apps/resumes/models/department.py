from django.db import models


class Department(models.Model):
    """Департамент"""
    title = models.CharField(
        verbose_name="Название подразделения",
        help_text="Введите подразделение",
        max_length=150,
        unique=True,
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
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"

    def __str__(self):
        return self.title
