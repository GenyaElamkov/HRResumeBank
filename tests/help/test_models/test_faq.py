from django.db import (
    IntegrityError,
    models,
)

import pytest

from core.apps.help.models.faq import FAQ
from core.apps.help.models.help_category import HelpCategory


class TestFAQModelStructure:
    """Проверка структуры модели FAQ"""

    def test_question(self, get_faq_field):
        """Проверка поля question"""
        field = get_faq_field(FAQ, 'question')
        assert isinstance(field, models.CharField)
        assert field.verbose_name == 'Вопрос'
        assert field.max_length == 500
        assert not field.blank
        assert not field.null

    def test_answer(self, get_faq_field):
        """Проверка поля answer"""
        field = get_faq_field(FAQ, 'answer')
        assert isinstance(field, models.TextField)
        assert field.verbose_name == 'Ответ'
        assert not field.blank
        assert not field.null

    def test_category(self, get_faq_field):
        """Проверка поля category"""
        field = get_faq_field(FAQ, 'category')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == HelpCategory
        assert field.verbose_name == 'Категория'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.remote_field.related_name == 'faqs'

    def test_is_published(self, get_faq_field):
        """Проверка поля is_published"""
        field = get_faq_field(FAQ, 'is_published')
        assert isinstance(field, models.BooleanField)
        assert field.verbose_name == 'Опубликовано'
        assert field.default is True

    def test_ordering(self, get_faq_field):
        """Проверка порядка сортировки"""
        field = get_faq_field(FAQ, 'order')
        assert isinstance(field, models.PositiveIntegerField)
        assert field.verbose_name == 'Порядок'
        assert field.default == 0


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
