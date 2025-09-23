import os

from django import forms
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models.card import Card


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


class CardFillForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._created_dinamic_fields()

    def _created_dinamic_fields(self):
        if not self.instance or not self.instance.template:
            return

        template_fields = self.instance.template.fields.all()

        for field in template_fields:
            field_name = field.title
            initial = self.instance.values.get(field_name)

            if field.field_type == "text":
                self.fields[field_name] = forms.CharField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                    widget=forms.Textarea,
                )
            elif field.field_type == "number":
                self.fields[field_name] = forms.IntegerField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                )
            elif field.field_type == "date":
                self.fields[field_name] = forms.DateField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                    widget=forms.DateInput(attrs={"type": "date"}),
                )
            elif field.field_type == "boolean":
                self.fields[field_name] = forms.BooleanField(
                    label=field_name,
                    required=False,
                    initial=initial,
                )
            elif field.field_type == "email":
                self.fields[field_name] = forms.EmailField(
                    label=field_name,
                    required=False,
                    initial=initial,
                )
            elif field.field_type == "choice":
                choices = [(c.strip(), c.strip()) for c in field.choices.split(",")]
                self.fields[field_name] = forms.ChoiceField(
                    label=field_name,
                    choices=choices,
                    required=field.is_required,
                    initial=initial,
                )
            elif field.field_type == "image":
                self.fields[field_name] = forms.ImageField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                )
            elif field.field_type == "file":
                self.fields[field_name] = forms.FileField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                )

    # TODO: Не удаляет значнеия в полях
    def save(self, commit=True):
        card = super().save(commit=False)

        for key, value in self.cleaned_data.items():
            if key not in ['csrfmiddlewaretoken']:
                if value:
                    if hasattr(value, 'read'):
                        path = default_storage.save(os.path.join("uploads", value.name), ContentFile(value.read()))
                        card.values[key] = os.path.join(settings.MEDIA_URL, path)
                    else:
                        card.values[key] = value
                else:
                    if key in card.values:
                        continue
                    else:
                        card.values[key] = None

        if commit:
            card.save()
        return card
