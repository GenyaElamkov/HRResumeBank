from django import forms

from tinymce.widgets import TinyMCE

from .models.card import Card
from .models.file_storage import FileStorage
from .models.profile_image import ProfileImage


class CardCreateForm(forms.ModelForm):
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
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CardFillForm(forms.ModelForm):
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
        self.fields[field_name] = forms.EmailField(
            label=field.title,
            required=field.is_required,
            initial=initial,
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
