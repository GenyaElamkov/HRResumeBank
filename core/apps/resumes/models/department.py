from django.db import models
from django.forms import ValidationError


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

    def clean(self):
        if self.parent == self:
            raise ValidationError("Department cannot be its own parent")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
