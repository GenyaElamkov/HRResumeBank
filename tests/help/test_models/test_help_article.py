from django.db import models

import pytest

from core.apps.help.models.help_article import HelpArticle
from core.apps.help.models.help_category import HelpCategory


class TestHelpArticleModelStructure:
    """Проверка структуры модели HelpArticle"""

    def test_availability_fields(self, get_fields):
        """Проверка наличие полей в модели"""
        fields = get_fields(HelpArticle)
        for field in fields:
            assert field.name in [
                'id',
                'create_at',
                'update_at',
                # Основные поля
                'title',
                'slug',
                'content',
                'short_description',
                'category',
                'tags',
                'is_published',
                'view_count',
                'order',
            ]

    @pytest.mark.parametrize(
        "field_name, field_type, field_attrs",
        [
            (
                "title", models.CharField, {
                        "verbose_name": "Заголовок",
                        "max_length": 300,
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "slug", models.SlugField, {
                        "verbose_name": "URL-адрес",
                        "unique": True,
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "content", models.TextField, {
                        "verbose_name": "Содержание",
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "short_description", models.TextField, {
                        "verbose_name": "Краткое описание",
                        "blank": True,
                        "null": False,
                },
            ),
            (
                "tags", models.CharField, {
                        "verbose_name": "Теги",
                        "max_length": 500,
                        "blank": True,
                        "null": False,
                        "help_text": "Разделяйте теги запятыми",
                },
            ),
            (
                "is_published", models.BooleanField, {
                        "verbose_name": "Опубликовано",
                        "default": True,
                        "null": False,
                        "blank": False,
                },
            ),
            (
                "view_count", models.PositiveIntegerField, {
                        "verbose_name": "Количество просмотров",
                        "default": 0,
                        "null": False,
                        "blank": False,
                },
            ),
            (
                "order", models.PositiveIntegerField, {
                        "verbose_name": "Порядок",
                        "default": 0,
                        "null": False,
                        "blank": False,
                },
            ),
        ],
    )
    def test_field_structure(self, get_field, field_name, field_type, field_attrs):
        """Проверка полей"""
        field = get_field(HelpArticle, field_name)
        assert isinstance(field, field_type)
        for attr, value in field_attrs.items():
            assert getattr(field, attr) == value

    def test_category(self, get_field):
        """Проверка поля category"""
        field = get_field(HelpArticle, 'category')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == HelpCategory
        assert field.verbose_name == 'Категория'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.remote_field.related_name == 'articles'


class TestHelpArticleMeta:
    """Проверка мета-класса модели HelpArticle"""

    def test_meta_verbose_name(self):
        """Проверка verbose_name"""
        verbose_name = HelpArticle._meta.verbose_name
        assert verbose_name == 'Статья справки'

    def test_meta_verbose_name_plural(self):
        """Проверка verbose_name_plural"""
        verbose_name_plural = HelpArticle._meta.verbose_name_plural
        assert verbose_name_plural == 'Статьи справки'

    def test_meta_db_table(self):
        """Проверка db_table"""
        db_table = HelpArticle._meta.db_table
        assert db_table == 'help_article'

    def test_meta_ordering(self):
        """Проверка ordering"""
        ordering = HelpArticle._meta.ordering
        assert ordering == ['order', 'title']


@pytest.mark.django_db
class TestHelpArticleBehavior:
    """Проверка поведения модели HelpArticle"""

    def test_str(self):
        """Проверка __str__"""
        article = HelpArticle(title='Тестовая статья')
        assert str(article) == 'Тестовая статья'

    def test_help_article_creation(self, help_category, help_article):
        """Проверка создания статьи"""
        assert help_article.title == 'Тестовая статья'
        assert help_article.slug == 'test-article'
        assert help_article.content == 'Тестовый контент'
        assert help_article.short_description == 'Тестовое описание'
        assert help_article.category == help_category
        assert help_article.tags == "тест, тестовый"
        assert help_article.is_published is True
        assert help_article.view_count == 0
        assert help_article.order == 1
