from django.test import TestCase
from django.urls import (
    resolve,
    reverse,
)

from core.apps.help.views import (
    FAQListView,
    HelpArticleView,
    HelpCategoryView,
    HelpHomeView,
    HelpSearchView,
)


class TestHelpUrls(TestCase):
    """Тестируем URL-адреса для приложения help"""

    def _assert_url_resolves_to_views(self, name, view_class, **kwargs):
        """Проверяем, что URL-адрес разрешается в нужный класс представления"""
        url = reverse(name, kwargs=kwargs)
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, view_class)

    def test_help_home(self):
        """Проверяем URL-адрес главной страницы помощи"""
        self._assert_url_resolves_to_views(
            name='help_system:help_home',
            view_class=HelpHomeView,
        )

    def test_help_search(self):
        """Проверяем URL-адрес поиска помощи"""
        self._assert_url_resolves_to_views(
            name='help_system:search',
            view_class=HelpSearchView,
        )

    def test_category(self):
        """Проверяем URL-адрес категории помощи"""
        self._assert_url_resolves_to_views(
            name='help_system:category',
            view_class=HelpCategoryView,
            slug='test-slug',
        )

    def test_article(self):
        """Проверяем URL-адрес статьи помощи"""
        self._assert_url_resolves_to_views(
            name='help_system:article',
            view_class=HelpArticleView,
            slug='test-slug',
        )

    def test_faq(self):
        """Проверяем URL-адрес FAQ"""
        self._assert_url_resolves_to_views(
            name='help_system:faq',
            view_class=FAQListView,
        )
