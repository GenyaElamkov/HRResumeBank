from django.db import models

import pytest

from core.apps.help.models.help_category import HelpCategory


class TestHelpCategoryStructure:
    """Проверка структуры модели HelpCategory"""

    def test_availability_fields(self, get_fields):
        """Проверка наличие полей в модели"""
        fields = get_fields(HelpCategory)
        for field in fields:
            assert field.name in [
                'faqs',
                'articles',
                'title',
                'children',
                'id',
                'create_at',
                'update_at',
                'slug',
                'description',
                'parent',
                'order',
                'is_active',
            ]

    def test_title(self, get_field):
        """Проверка поля title"""
        field = get_field(HelpCategory, 'title')
        assert isinstance(field, models.CharField)
        assert field.verbose_name == 'Название категории'
        assert field.max_length == 200
        assert field.blank is False
        assert field.null is False

    def test_slug(self, get_field):
        """Проверка поля slug"""
        field = get_field(HelpCategory, 'slug')
        assert isinstance(field, models.SlugField)
        assert field.verbose_name == 'URL-адрес'
        assert field.unique is True
        assert field.blank is False
        assert field.null is False

    def test_description(self, get_field):
        """Проверка поля description"""
        field = get_field(HelpCategory, 'description')
        assert isinstance(field, models.TextField)
        assert field.verbose_name == 'Описание'
        assert field.blank is True
        assert field.null is False

    def test_parent(self, get_field):
        """Проверка поля parent"""
        field = get_field(HelpCategory, 'parent')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == HelpCategory
        assert field.verbose_name == 'Родительская категория'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.null is True
        assert field.blank is True
        assert field.remote_field.related_name == 'children'

    def test_order(self, get_field):
        """Проверка поля order"""
        field = get_field(HelpCategory, 'order')
        assert isinstance(field, models.PositiveIntegerField)
        assert field.verbose_name == 'Порядок'
        assert field.default == 0
        assert field.blank is False
        assert field.null is False

    def test_is_active(self, get_field):
        """Проверка поля is_active"""
        field = get_field(HelpCategory, 'is_active')
        assert isinstance(field, models.BooleanField)
        assert field.verbose_name == 'Активна'
        assert field.default is True
        assert field.blank is False
        assert field.null is False


class TestHelpCategoryMeta:
    """Проверка мета класса HelpCategory"""

    def test_meta_verbose_name(self):
        """Проверка verbose_name"""
        verbose_name = HelpCategory._meta.verbose_name
        assert verbose_name == 'Категория справки'

    def test_meta_verbose_name_plural(self):
        """Проверка verbose_name_plural"""
        verbose_name_plural = HelpCategory._meta.verbose_name_plural
        assert verbose_name_plural == 'Категории справки'

    def test_meta_db_table(self):
        """Проверка db_table"""
        db_table = HelpCategory._meta.db_table
        assert db_table == 'help_category'

    def test_meta_ordering(self):
        """Проверка ordering"""
        ordering = HelpCategory._meta.ordering
        assert ordering == ['order', 'title']


@pytest.mark.django_db
class TestHelpCategoryBehavior:
    """Проверка поведения модели HelpCategory"""

    def test_str(self):
        """Проверка __str__"""
        category = HelpCategory(title='Тестовая категория')
        assert str(category) == 'Тестовая категория'

    def test_help_category_creating(self, help_category):
        """Проверка создания категории"""
        assert help_category.title == 'Тестовая категория'
        assert help_category.slug == 'testovoy-kategoriya'
        assert help_category.description == 'Описание тестовой категории'
        assert help_category.order == 1
        assert help_category.is_active is True
