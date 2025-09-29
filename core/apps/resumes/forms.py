from django import forms

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
        card.save()

        for key, value in self.cleaned_data.items():
            if key in ['csrfmiddlewaretoken']:
                continue

            # Обработка изображений
            if value and hasattr(value, 'read') and key in [
                field.title for field in card.template.fields.all() if field.field_type == "image"
            ]:
                profile_image = ProfileImage(card=card, image=value)
                profile_image.save()
                card.values[key] = profile_image.image.name

            # Обработка файлов
            elif value and hasattr(value, 'read'):
                file_storage = FileStorage(card=card, uploaded_file=value)
                file_storage.save()
                card.values[key] = file_storage.uploaded_file.name
            else:
                card.values[key] = value

        if commit:
            card.save()
        return card
