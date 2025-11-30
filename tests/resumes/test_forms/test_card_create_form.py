import pytest

from core.apps.resumes.forms import CardCreateForm
from core.apps.resumes.models.card import Card


class TestCardCreateFormMeta:
    """Проверка мета класса формы создания карточки"""

    def test_meta_model(self):
        assert CardCreateForm.Meta.model is Card

    def test_meta_fields(self):
        assert CardCreateForm.Meta.fields == ['template']

    def test_available_fields(self):
        fields = CardCreateForm._meta.fields
        for field in fields:
            assert field in ['template']


@pytest.mark.django_db
class TestCardCreateForm:
    """Проверка формы создания карточки"""

    def test_form_save(self, template, custom_user):
        form_data = {"template": template.pk}
        form = CardCreateForm(data=form_data, created=custom_user)
        assert form.is_valid(), form.errors

        card = form.save(commit=True)
        assert card.values == {}
        assert card.created == custom_user
