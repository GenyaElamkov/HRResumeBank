import pytest

from core.apps.accounts.models import CustomUser


@pytest.fixture
def user_factory():
    """Фабрика для создания пользователей"""
    def create_user(username, **kwargs):
        return CustomUser.objects.create_user(
            username=username,
            **kwargs,
        )
    return create_user


@pytest.fixture
def sample_users(user_factory):
    """Фикстура с набором тестовых пользователей"""
    return {
        'full_name': user_factory(
            username="user1",
            first_name="Иван",
            last_name="Иванов",
            surname="Иванович",
        ),
        'no_surname': user_factory(
            username="user2",
            first_name="Иван",
            last_name="Иванов",
            surname="",
        ),
        'only_first_name': user_factory(
            username="user3",
            first_name="Иван",
            last_name="",
            surname="",
        ),
        'empty_names': user_factory(
            username="user4",
            first_name="",
            last_name="",
            surname="",
        ),
        'no_first_name': user_factory(
            username="user5",
            first_name="",
            last_name="Иванов",
            surname="Иванович",
        ),
        'only_surname': user_factory(
            username="user6",
            first_name="",
            last_name="",
            surname="Иванович",
        ),
        'no_last_name': user_factory(
            username="user7",
            first_name="Иван",
            last_name="",
            surname="Иванович",
        ),
    }
