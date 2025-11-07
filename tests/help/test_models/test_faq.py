from django.db import (
    IntegrityError,
    models,
)

import pytest

from core.apps.help.models.faq import FAQ
from core.apps.help.models.help_category import HelpCategory


class TestFAQModelStructure:
    """Проверка структуры модели FAQ"""

    def test_availability_fields(self, get_fields):
        """Проверка наличие полей в модели"""
        fields = get_fields(FAQ)
        for field in fields:
            assert field.name in [
                'id',
                'create_at',
                'update_at',
                'question',
                'answer',
                'category',
                'is_published',
                'order',
            ]

    @pytest.mark.parametrize(
        "field_name, field_type, field_attrs",
        [
            (
                "question", models.CharField, {
                        "verbose_name": "Вопрос",
                        "max_length": 500,
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "answer", models.TextField, {
                        "verbose_name": "Ответ",
                        "blank": False,
                        "null": False,
                },
            ),
            (
                "is_published", models.BooleanField, {
                        "verbose_name": "Опубликовано",
                        "default": True,
                },
            ),
            (
                "order", models.PositiveIntegerField, {
                        "verbose_name": "Порядок",
                        "default": 0,
                },
            ),
        ],
    )
    def test_field_structure(self, get_field, field_name, field_type, field_attrs):
        """Проверка полей"""
        field = get_field(FAQ, field_name)
        assert isinstance(field, field_type)
        for attr, value in field_attrs.items():
            assert getattr(field, attr) == value

    def test_category(self, get_field):
        """Проверка поля category"""
        field = get_field(FAQ, 'category')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == HelpCategory
        assert field.verbose_name == 'Категория'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.remote_field.related_name == 'faqs'


@pytest.mark.django_db
class TestFAQBehavior:
    """Проверка поведения модели FAQ"""

    def test_faq_creation(self, faq, help_category):
        """Проверка создания FAQ"""
        assert faq.question == "Тестовый вопрос"
        assert faq.answer == "Тестовый ответ"
        assert faq.category == help_category
        assert faq.is_published is True
        assert faq.order == 1

    def test_question_required(self, help_category):
        """Проверка обязательности поля question"""
        with pytest.raises(IntegrityError):
            FAQ.objects.create(question=None, answer="Ответ", category=help_category)

    def test_str(self):
        """Проверка __str__ метода"""
        assert str(FAQ(question='Тестовые данные')) == 'Тестовые данные'


class TestFAQMeta:
    """Проверка мета класса FAQ"""

    def test_meta_verbose_name(self):
        """Проверка мета класса verbose_name"""
        verbose_name = FAQ._meta.verbose_name
        assert verbose_name == 'Часто задаваемый вопрос'

    def test_meta_verbose_name_plural(self):
        """Проверка мета класса verbose_name_plural"""
        verbose_name_plural = FAQ._meta.verbose_name_plural
        assert verbose_name_plural == 'Часто задаваемые вопросы'

    def test_meta_db_table(self):
        """Проверка мета класса db_table"""
        db_table = FAQ._meta.db_table
        assert db_table == 'help_faq'

    def test_meta_ordering(self):
        """Проверка мета класса ordering"""
        ordering = FAQ._meta.ordering
        assert ordering == ['order', 'question']
