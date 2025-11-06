import pytest

from core.apps.help.models.faq import FAQ
from core.apps.help.models.help_article import HelpArticle
from core.apps.help.models.help_category import HelpCategory


@pytest.fixture
def get_faq_field():
    """Фикстура поля модели"""
    def _get_field(model, field_name):
        return model._meta.get_field(field_name)
    return _get_field


@pytest.fixture
def help_category():
    """Фикстура категории помощи"""
    return HelpCategory.objects.create(
            title="Техническая поддержка",
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
