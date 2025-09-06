from django.db import models


class EntityData(models.Model):
    """Значения динамических полей"""

    entity = models.ForeignKey(
        to="resumes.Entity",
        verbose_name="К какой сущности относится значение",
        on_delete=models.CASCADE,
        related_name="date_entitydate",
    )
    field = models.ForeignKey(
        to="resumes.TemplateField",
        verbose_name="К какому полю относится значение",
        on_delete=models.CASCADE,
        related_name="field_entitydate",
    )
    value_text = models.TextField(
        verbose_name="Значение текстового поля",
        blank=True,
        null=True,
    )
    value_number = models.IntegerField(
        verbose_name="Числовое значение",
        blank=True,
        null=True,
    )
    value_date = models.DateField(
        verbose_name="Дата",
        blank=True,
        null=True,
    )
    value_email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True,
    )
    value_images = models.ImageField(
        verbose_name="Картинка",
        upload_to="images/",
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
        db_table = "entity_data"

        indexes = [
            models.Index(fields=['value_text', 'value_number', 'value_date']),
        ]
