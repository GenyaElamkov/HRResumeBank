from django.urls import (
    resolve,
    Resolver404,
    reverse,
)

import pytest

from core.apps.authentication.views import logout_everywhere


class TestAuthenticationURLs:
    """Тестируем URL-конфигурацию приложения authentication."""

    @pytest.mark.parametrize(
        "url_path, url_name, expected_view_attr",
        [
            ("/auth/login/", "authentication:login", "LoginView"),
            ("/auth/logout/", "authentication:logout", logout_everywhere),
            ("/auth/locked/", "authentication:locked", "TemplateView"),
        ],
    )
    def test_url_resolves_to_correct_view(self, url_path, url_name, expected_view_attr):
        """Проверяем, что URL разрешается в ожидаемое представление."""
        try:
            resolved = resolve(url_path)
        except Resolver404:
            pytest.fail(f"URL {url_path} не найден в маршрутах")

        # Определяем реальное представление
        if hasattr(resolved.func, "view_class"):
            actual_view = resolved.func.view_class
        else:
            actual_view = resolved.func

        if isinstance(expected_view_attr, str):
            assert actual_view.__name__ == expected_view_attr, (
                f"Ожидался класс с именем {expected_view_attr}, но получено {actual_view.__name__}"
            )
        else:
            assert actual_view == expected_view_attr, (
                f"Ожидалось представление {expected_view_attr}, но получено {actual_view}"
            )

        # Проверяем, что reverse работает
        assert reverse(url_name) == url_path, (
            f"reverse({url_name}) должен возвращать {url_path}, но вернул {reverse(url_name)}"
        )

    @pytest.mark.parametrize(
        "url_path, expected_template",
        [
            ("/auth/login/", "authentication/login.html"),
            ("/auth/locked/", "authentication/locked.html"),
        ],
    )
    def test_url_views_use_correct_template(self, url_path, expected_template):
        """Проверяем, что представления используют ожидаемые шаблоны."""
        resolved = resolve(url_path)
        if not hasattr(resolved.func, "view_class"):
            pytest.skip("Представление не является классом, пропускаем проверку шаблона")

        view_class = resolved.func.view_class
        view_initkwargs = resolved.func.view_initkwargs

        # Проверяем template_name только если он явно задан в инициализации
        if "template_name" in view_initkwargs:
            assert view_initkwargs["template_name"] == expected_template
        else:
            # Проверяем, есть ли атрибут по умолчанию в классе
            assert getattr(view_class, "template_name", None) == expected_template, (
                f"Шаблон для {view_class.__name__} не соответствует ожидаемому"
            )

    @pytest.mark.parametrize(
        "url_path, expected_redirect_flag",
        [
            ("/auth/login/", True),
        ],
    )
    def test_login_view_redirect_authenticated_user(self, url_path, expected_redirect_flag):
        """Проверяем параметр redirect_authenticated_user для LoginView."""
        resolved = resolve(url_path)
        assert resolved.func.view_initkwargs.get("redirect_authenticated_user") is expected_redirect_flag
