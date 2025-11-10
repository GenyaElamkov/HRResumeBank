import pytest

from core.apps.accounts.models import CustomUser
from core.apps.help.models.faq import FAQ
from core.apps.help.models.help_article import HelpArticle
from core.apps.help.models.help_category import HelpCategory
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template
from core.apps.resumes.models.template_field import TemplateField


@pytest.fixture
def get_field():
    """Фикстура поля модели"""
    def _get_field(model, field_name):
        return model._meta.get_field(field_name)
    return _get_field


@pytest.fixture
def get_fields():
    """Фикстура полей модели"""
    def _get_fields(model):
        return model._meta.get_fields(include_parents=False)
    return _get_fields


@pytest.fixture
def help_category():
    """Фикстура категории помощи"""
    return HelpCategory.objects.create(
            title="Тестовая категория",
            slug="testovoy-kategoriya",
            description="Описание тестовой категории",
            order=1,
            is_active=True,
    )


@pytest.fixture
def faq(help_category):
    """Фикстура FAQ"""
    return FAQ.objects.create(
            question="Тестовый вопрос",
            answer="Тестовый ответ",
            category=help_category,
            is_published=True,
            order=1,
    )


@pytest.fixture
def help_article(help_category):
    """Фикстура статьи помощи"""
    return HelpArticle.objects.create(
            title="Тестовая статья",
            slug="test-article",
            content="Тестовый контент",
            short_description="Тестовое описание",
            category=help_category,
            tags="тест, тестовый",
            is_published=True,
            view_count=0,
            order=1,
    )


@pytest.fixture
def template():
    """Фикстура шаблона"""
    return Template.objects.create(
            title="Тестовый шаблон",
            description="Описание тестового шаблона",
    )


@pytest.fixture
def template_field(template):
    """Фикстура поля шаблона"""
    return TemplateField.objects.create(
            template=template,
            title="Тестовое поле",
            field_type="text",
            description="Описание тестового поля",
            is_pimable=True,
            order=1,
    )


@pytest.fixture
def custom_user():
    """Фикстура пользователя"""
    return CustomUser.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
    )


@pytest.fixture
def card(template, custom_user):
    """Фикстура карты"""
    return Card.objects.create(
        template=template,
        created=custom_user,
        values={
            "name": "Тестовое имя",
            "job": "Тестовый профессия",
        },

    )
