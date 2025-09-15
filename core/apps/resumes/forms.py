from django import forms

from .models.card import Card


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["template"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("created")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        card = super().save(commit=False)
        card.created = self.user
        card.values = {}
        if commit:
            card.save()
        return card


class CardFillForm(forms.Form):
    def __init__(self, card: Card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card = card
        self.template_fields = card.template.fields.all()

        for field in self.template_fields:
            field_name = field.title
            initial = card.values.get(field_name)

            if field.field_type == "text":
                self.fields[field_name] = forms.CharField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                )
            elif field.field_type == "number":
                self.fields[field_name] = forms.IntegerField(
                    label=field_name,
                    required=field.is_required,
                    initial=initial,
                )
            elif field.field_type == "date":
                self.fields[field_name] = forms.DateField(
                    label=field_name, required=field.is_required, initial=initial,
                    widget=forms.DateInput(attrs={"type": "date"}),
                )
            elif field.field_type == "bool":
                self.fields[field_name] = forms.BooleanField(label=field_name, required=False, initial=initial)
            elif field.field_type == "choice":
                choices = [(c.strip(), c.strip()) for c in field.choices.split(",")]
                self.fields[field_name] = forms.ChoiceField(
                    label=field_name,
                    choices=choices,
                    required=field.is_required,
                    initial=initial,
                )

    def save(self):
        for key, value in self.cleaned_data.items():
            self.card.values[key] = value
        self.card.save()
        return self.card
