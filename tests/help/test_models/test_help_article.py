from django.db import models

import pytest

from core.apps.help.models.help_article import HelpArticle
from core.apps.help.models.help_category import HelpCategory


class TestHelpArticleModelStructure:
    """Проверка структуры модели HelpArticle"""

    def test_title(self, get_field):
        """Проверка поля title"""
        field = get_field(HelpArticle, 'title')
        assert isinstance(field, models.CharField)
        assert field.verbose_name == 'Заголовок'
        assert field.max_length == 300
        assert not field.blank
        assert not field.null

    def test_slug(self, get_field):
        """Проверка поля slug"""
        field = get_field(HelpArticle, 'slug')
        assert isinstance(field, models.SlugField)
        assert field.verbose_name == 'URL-адрес'
        assert field.unique is True
        assert not field.blank
        assert not field.null

    def test_content(self, get_field):
        """Проверка поля content"""
        field = get_field(HelpArticle, 'content')
        assert isinstance(field, models.TextField)
        assert field.verbose_name == 'Содержание'
        assert not field.blank
        assert not field.null

    def test_short_description(self, get_field):
        """Проверка поля short_description"""
        field = get_field(HelpArticle, 'short_description')
        assert isinstance(field, models.TextField)
        assert field.verbose_name == 'Краткое описание'
        assert field.blank is True
        assert field.null is False

    def test_category(self, get_field):
        """Проверка поля category"""
        field = get_field(HelpArticle, 'category')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == HelpCategory
        assert field.verbose_name == 'Категория'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.remote_field.related_name == 'articles'

    def test_tags(self, get_field):
        """Проверка поля tags"""
        field = get_field(HelpArticle, 'tags')
        assert isinstance(field, models.CharField)
        assert field.verbose_name == 'Теги'
        assert field.max_length == 500
        assert field.blank is True
        assert field.null is False
        assert field.help_text == 'Разделяйте теги запятыми'

    def test_is_published(self, get_field):
        """Проверка поля is_published"""
        field = get_field(HelpArticle, 'is_published')
        assert isinstance(field, models.BooleanField)
        assert field.verbose_name == 'Опубликовано'
        assert field.default is True
        assert field.null is False
        assert field.blank is False

    def test_view_count(self, get_field):
        """Проверка поля view_count"""
        field = get_field(HelpArticle, 'view_count')
        assert isinstance(field, models.PositiveIntegerField)
        assert field.verbose_name == 'Количество просмотров'
        assert field.default == 0
        assert field.null is False
        assert field.blank is False

    def test_order(self, get_field):
        """Проверка поля order"""
        field = get_field(HelpArticle, 'order')
        assert isinstance(field, models.PositiveIntegerField)
        assert field.verbose_name == 'Порядок'
        assert field.default == 0
        assert field.null is False
        assert field.blank is False


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
