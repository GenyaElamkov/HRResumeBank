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
                'id',
                'create_at',
                'update_at',
                'faqs',
                'articles',
                'children',
                # Основные поля
                'title',
                'slug',
                'description',
                'parent',
                'order',
                'is_active',
            ]

    @pytest.mark.parametrize(
        "field_name, field_type, field_attrs",
        [
            (
                "title", models.CharField, {
                        "verbose_name": "Название категории",
                        "max_length": 200,
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
                "description", models.TextField, {
                        "verbose_name": "Описание",
                        "blank": True,
                        "null": False,
                },
            ),
            (
                "order", models.PositiveIntegerField, {
                        "verbose_name": "Порядок",
                        "default": 0,
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "is_active", models.BooleanField, {
                        "verbose_name": "Активна",
                        "default": True,
                        "blank": False,
                        "null": False,
                },
            ),
        ],
    )
    def test_field_structure(self, get_field, field_name, field_type, field_attrs):
        """Проверка полей"""
        field = get_field(HelpCategory, field_name)
        assert isinstance(field, field_type)
        for attr, value in field_attrs.items():
            assert getattr(field, attr) == value

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
