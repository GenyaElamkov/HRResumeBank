from django.db import models

import pytest

from core.apps.accounts.models import CustomUser


@pytest.mark.django_db
class TestCustomUser:
    """Проверка модели CustomUser"""

    def test_surname_field(self):
        """Проверка поля surname"""
        field = CustomUser._meta.get_field("surname")
        assert isinstance(field, models.CharField)
        assert field.verbose_name == "Отчество"
        assert field.max_length == 150
        assert field.blank is True
        assert field.null is True

    def test_get_full_name_complete(self, sample_users):
        """Проверка полного ФИО"""
        user = sample_users['full_name']
        assert user.get_full_name() == "Иван Иванович Иванов"

    def test_get_full_name_without_surname(self, sample_users):
        """Проверка ФИО без отчества"""
        user = sample_users['no_surname']
        assert user.get_full_name() == "Иван Иванов"

    def test_get_full_name_only_first_name(self, sample_users):
        """Проверка ФИО без фамилии, отчества"""
        user = sample_users['only_first_name']
        assert user.get_full_name() == "user3"

    def test_get_full_name_empty_names(self, sample_users):
        """Проверка ФИО без данных"""
        user = sample_users['empty_names']
        assert user.get_full_name() == "user4"

    def test_get_full_name_no_first_name(self, sample_users):
        """Проверка ФИО без имени"""
        user = sample_users['no_first_name']
        assert user.get_full_name() == "user5"

    def test_get_full_name_only_surname(self, sample_users):
        """Проверка ФИО без имени и отчества"""
        user = sample_users['only_surname']
        assert user.get_full_name() == "user6"

    def test_get_full_name_no_last_name(self, sample_users):
        """Проверка ФИО без фамилии"""
        user = sample_users['no_last_name']
        assert user.get_full_name() == "user7"

    def test_meta(self):
        """Проверка мета-класса"""
        verbose_name = CustomUser._meta.verbose_name
        assert verbose_name == "Пользователь"

        verbose_name_plural = CustomUser._meta.verbose_name_plural
        assert verbose_name_plural == "Пользователи"

        db_table = CustomUser._meta.db_table
        assert db_table == "custom_user"

        indexes = CustomUser._meta.indexes
        username_index = None
        email_index = None
        for index in indexes:
            if index.fields == ['username']:
                username_index = index
            elif index.fields == ['email']:
                email_index = index
        assert username_index is not None
        assert email_index is not None
