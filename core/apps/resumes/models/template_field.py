from django.db import models


class TemplateField(models.Model):
    """Поля шаблона"""

    class TypeField(models.TextChoices):
        """Тип поля"""

        TEXT = "text", "Текст"
        NUMBER = "number", "Число"
        DATE = "date", "Дата"
        BOOLEAN = "boolean", "Булево"
        EMAIL = "email", "Почта"
        CHOICE = "choice", "Выбор"
        IMAGE = "image", "Изображение"
        FILE = "file", "Файл"

    template = models.ForeignKey(
        to="resumes.Template",
        verbose_name="Шаблон, которому принадлежит поле",
        on_delete=models.CASCADE,
        related_name="fields",
    )
    title = models.CharField(
        verbose_name="Имя поля",
        max_length=100,
    )
    field_type = models.CharField(
        verbose_name="Тип данных",
        max_length=50,
        choices=TypeField.choices,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    choices = models.TextField(
        verbose_name="Поле выбора",
        help_text="Введите значения, разделеными запятыми",
        blank=True,
    )
    is_required = models.BooleanField(
        verbose_name="Обязательность заполнения",
        default=False,
    )
    is_primary = models.BooleanField(
        help_text="Если отмечено — это поле используется как 'главное' \
            для отображения в загаловке карточки (например ФИО или Название компании).",
        default=False,
    )
    is_visible = models.BooleanField(
        help_text="Если отмечено — это поле будет видно \
            в карточке резюме на главном экране",
        default=False,
    )
    order = models.PositiveSmallIntegerField(
        verbose_name="Порядок",
        help_text="Порядок отображения в карточке",
        default=0,
    )

    def __str__(self):
        return f"{self.template} -> {self.title}"

    class Meta:
        verbose_name = "Полe шаблона"
        verbose_name_plural = "Поля шаблона"
        db_table = "template_field"
        ordering = ['order']
