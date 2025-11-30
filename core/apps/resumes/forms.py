import os
from dataclasses import dataclass
from typing import List

from django import forms
from django.core.validators import validate_email

from tinymce.widgets import TinyMCE

from .models.card import Card
from .models.file_storage import FileStorage
from .models.profile_image import ProfileImage


@dataclass
class FieldValidationConfig:
    allowed_extensions: List[str]


RESUME_FILE_CONFIG = FieldValidationConfig(
    allowed_extensions=[
        ".pdf", ".docx", ".doc", ".txt", ".jpg", ".jpeg", ".png", ".xlsx", ".xls",
    ],
)


class CardCreateForm(forms.ModelForm):
    """Форма для создания карточки на основе выбранного шаблона"""
    class Meta:
        model = Card
        fields = ["template"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('created', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        card = super().save(commit=False)
        if self.user:
            card.created = self.user
        card.values = {}
        if commit:
            card.save()
        return card


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для множественной загрузки файлов в формах"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле формы для загрузки несколько файлов одновременно"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        self.allowed_extensions = kwargs.pop(
            "allowed_extensions",
            RESUME_FILE_CONFIG.allowed_extensions,
        )
        super().__init__(*args, **kwargs)

    def validate(self, value):
        super().validate(value)
        if not value:
            return

        if not isinstance(value, (list, tuple)):
            value = [value]

        for file in value:
            ext = os.path.splitext(file.name)[1]
            if ext not in self.allowed_extensions:
                raise forms.ValidationError(
                    f"Файл '{file}' имеет недопустимое расширение '{ext}'. "
                    f"Разрешены: {', '.join(self.allowed_extensions)}",
                )

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultipleEmailField(forms.Field):
    """Поле формы для ввода нескольких email-адресов через запятую"""

    def to_python(self, value):
        """Нормализация данных в список email'ов"""
        if not value:
            return ''
        return [email.strip() for email in value.split(',') if email.strip()]

    def validate(self, value):
        """Проверка валидности всех email'ов"""
        super().validate(value)
        for email in value:
            validate_email(email)

    def prepare_value(self, value):
        """Преобразование значения для отображения в форме"""
        if isinstance(value, list):
            return ', '.join(value)
        return value

    def clean(self, value):
        data = super().clean(value)
        # Возвращаем строку для сохранения в БД
        return ', '.join(data) if isinstance(data, list) else data


class CardFillForm(forms.ModelForm):
    """Форма для заполнения карточки с динамически создаваемыми полями на основе шаблона"""

    class Meta:
        model = Card
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._created_dinamic_fields()

    def _add_text_field(self, field, field_name: str, initial):
        self.fields[field_name] = forms.CharField(
            label=field.title,
            required=field.is_required,
            initial=initial,
            widget=TinyMCE(
                attrs={'cols': 100, 'rows': 10},
            ),
        )

    def _add_number_field(self, field, field_name: str, initial):
        self.fields[field_name] = forms.IntegerField(
            label=field.title,
            required=field.is_required,
            initial=initial,
        )

    def _add_date_field(self, field, field_name: str, initial):
        self.fields[field_name] = forms.DateField(
            label=field.title,
            required=field.is_required,
            initial=initial,
            widget=forms.DateInput(
                attrs={
                    "type": "date",
                },
            ),
        )

    def _add_boolean_field(self, field, field_name: str, initial):
        self.fields[field_name] = forms.BooleanField(
            label=field.title,
            required=field.is_required,
            initial=initial,
            widget=forms.CheckboxInput(
                # Bootstrap
                attrs={
                    'class': 'form-check-input',
                },
            ),
        )

    def _add_email_field(self, field, field_name: str, initial):
        self.fields[field_name] = MultipleEmailField(
            label=field.title,
            required=field.is_required,
            initial=initial,
            help_text="Введите email-адреса через запятую",
        )

    def _add_choice_field(self, field, field_name: str, initial):
        choices = [(c.strip(), c.strip()) for c in field.choices.split(",")]
        self.fields[field_name] = forms.ChoiceField(
            label=field.title,
            choices=choices,
            required=field.is_required,
            initial=initial,
        )

    def _add_image_field(self, field, field_name: str, initial):
        self.fields[field_name] = forms.ImageField(
            label=field.title,
            required=field.is_required,
            initial=initial,
        )

    def _add_file_field(self, field, field_name: str, initial):
        self.fields[field_name] = MultipleFileField(
            label=field.title,
            required=field.is_required,
            initial=initial,
            help_text=f"Выберите файлы для загрузки. Разрешены: {", ".join(RESUME_FILE_CONFIG.allowed_extensions)}",
            allowed_extensions=RESUME_FILE_CONFIG.allowed_extensions,
        )

    def _created_dinamic_fields(self):
        if not self.instance or not self.instance.template:
            return

        template_fields = self.instance.template.fields.all()

        for field in template_fields:
            # для редактора текста в TinyMCE
            field_name = field.title.replace(' ', '_')

            initial = self.instance.values.get(field.title)

            if field.field_type == "text":
                self._add_text_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "number":
                self._add_number_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "date":
                self._add_date_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "boolean":
                self._add_boolean_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "email":
                self._add_email_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "choice":
                self._add_choice_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "image":
                self._add_image_field(field_name=field_name, field=field, initial=initial)

            elif field.field_type == "file":
                self._add_file_field(field_name=field_name, field=field, initial=initial)

    def save(self, commit=True):
        card = super().save(commit=False)
        card.save()

        for key, value in self.cleaned_data.items():
            if key in ['csrfmiddlewaretoken']:
                continue

            # для сохранения изображений в values
            key = key.replace('_', ' ')

            # Обработка изображений
            if value and hasattr(value, 'read') and key in [
                field.title for field in card.template.fields.all() if field.field_type == "image"
            ]:
                profile_image = ProfileImage(card=card, image=value)
                profile_image.save()
                card.values[key] = profile_image.image.name

            # Обработка файлов
            elif key in [
                field.title for field in card.template.fields.all() if field.field_type == "file"
            ]:
                if isinstance(value, list):
                    file_names = []
                    for file in value:
                        if file and hasattr(file, 'read'):
                            file_storage = FileStorage(card=card, uploaded_file=file)
                            file_storage.save()
                            file_names.append(file_storage.uploaded_file.name)
                    card.values[key] = file_names

                elif value and hasattr(value, 'read'):
                    file_storage = FileStorage(card=card, uploaded_file=value)
                    file_storage.save()
                    card.values[key] = file_storage.uploaded_file.name
            else:
                card.values[key] = value

        if commit:
            card.save()
        return card
