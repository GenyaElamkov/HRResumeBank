from django.db import models

from core.apps.resumes.models.entity import Entity
from core.apps.resumes.models.template_field import TemplateField


class EntityDate(models.Model):
    """Значения динамических полей"""

    entity = models.ForeignKey(
        Entity,
        verbose_name="К какой сущности относится значение",
        on_delete=models.CASCADE,
        related_name="date_entitydate",
    )
    field = models.ForeignKey(
        TemplateField,
        verbose_name="К какому полю относится значение",
        on_delete=models.CASCADE,
        related_name="field_entitydate",
    )
    value_text = models.TextField(
        verbose_name="Значение текстового поля",
        blank=True,
        null=True,
    )
    # TODO: Поменять Decimal
    value_number = models.DecimalField(
        verbose_name="Числовое значение",
        max_digits=20,
        decimal_places=4,
        blank=True,
        null=True,
    )
    value_date = models.DateField(
        verbose_name="Дата",
        blank=True,
        null=True,
    )
    value_boolean = models.BooleanField(
        verbose_name="Булево значение",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.entity.template}: {self.field.title}"


    class Meta:
        verbose_name = "Значения динамического поля"
        verbose_name_plural = "Значения динамических полей"

        indexes = [
            models.Index(fields=['value_text', 'value_number', 'value_date',]),
        ]