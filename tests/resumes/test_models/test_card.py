from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

import pytest

from core.apps.accounts.models import CustomUser
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template


class TestCardModelStructure:
    """Проверка структуры модели Card"""

    def test_availability_fields(self, get_fields):
        """Проверка наличие полей в модели"""
        fields = get_fields(Card)
        for field in fields:
            assert field.name in [
                'id',
                'create_at',
                'update_at',
                'storage',
                'profile_image',
                # Основные поля
                'template',
                'created',
                'values',
                'main_name',
            ]

    @pytest.mark.parametrize(
        "field_name, field_type, field_attrs",
        [
            (
                'values', models.JSONField, {
                    'verbose_name': 'Значения полей',
                    'encoder': DjangoJSONEncoder,
                    'default': dict,
                },
            ),
            (
                'main_name', models.CharField, {
                    'verbose_name': 'Наименование карточки',
                    'max_length': 255,
                    'blank': True,
                    'null': True,
                    'editable': False,
                },
            ),
        ],
    )
    def test_field_structure(self, get_field, field_name, field_type, field_attrs):
        """Проверка структуры полей модели"""
        field = get_field(Card, field_name)
        assert isinstance(field, field_type)
        for attr, value in field_attrs.items():
            assert getattr(field, attr) == value

    def test_tempate_field(self, get_field):
        """Проверка поля template"""
        field = get_field(Card, 'template')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == Template
        assert field.verbose_name == 'Шаблон'
        assert field.remote_field.on_delete == models.CASCADE
        assert field.remote_field.related_name == 'cards'

    def test_created_field(self, get_field):
        """Проверка поля created"""
        field = get_field(Card, 'created')
        assert isinstance(field, models.ForeignKey)
        assert field.related_model == CustomUser
        assert field.verbose_name == 'Кто создал запись'
        assert field.remote_field.on_delete == models.PROTECT
        assert field.remote_field.related_name == 'created_card'


class TestCardMeta:
    """Проверка мета-класса модели Card"""
    def test_meta_verbose_name(self):
        """Проверка verbose_name"""
        verbose_name = Card._meta.verbose_name
        assert verbose_name == 'Карточка'

    def test_meta_verbose_name_plural(self):
        """Проверка verbose_name_plural"""
        verbose_name_plural = Card._meta.verbose_name_plural
        assert verbose_name_plural == 'Карточки'

    def test_meta_db_table(self):
        """Проверка db_table"""
        db_table = Card._meta.db_table
        assert db_table == 'card'

    def test_meta_ordering(self):
        """Проверка ordering"""
        ordering = Card._meta.ordering
        assert ordering == ['-create_at']


@pytest.mark.django_db
class TestCardBehaviour:
    """Проверка поведения модели Card"""

    def test_card_create(self, card):
        """Проверка создание Card"""
        assert card.created.id is not None
        assert card.template is not None
        assert card.values == {
            "name": "Тестовое имя",
            "job": "Тестовый профессия",
        }
        assert card.main_name == "Тестовый шаблон #1"

    def test_str(self, card):
        """Проверка __str__"""
        assert str(card) == "Тестовый шаблон Карточка #1"
