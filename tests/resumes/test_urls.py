from django.test import TestCase
from django.urls import (
    resolve,
    reverse,
)
from django.urls.exceptions import Resolver404

from core.apps.resumes.views import (
    AdvancedCardSearchView,
    CardCreateView,
    CardDetailView,
    CardListView,
    CardUpdateView,
    FileDeleteView,
    HomeScreenCardSearchView,
    ImageDeleteView,
)


class TestResumesUrls(TestCase):
    """Тестируем URL-адреса для карточек"""
    def _assert_url_resolves_to_views(self, name, view_class, **kwargs):
        """Проверяем, что URL-адрес разрешается в нужный класс представления"""
        url = reverse(name, kwargs=kwargs)
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, view_class)

    def _assert_url_raises_404(self, url, **kwargs):
        """Проверяем, что URL-адрес возвращает 404"""
        with self.assertRaises(Resolver404):
            resolve(url)

    def test_card_list_url(self):
        """Проверяем URL-адрес списка карточек"""
        self._assert_url_resolves_to_views(
            name='resumes:card_list',
            view_class=CardListView,
        )

    def test_card_create_url(self):
        """Проверяем URL-адрес создания карточки"""
        self._assert_url_resolves_to_views(
            name='resumes:create_card',
            view_class=CardCreateView,
        )

    def test_card_update_url(self):
        """Проверяем URL-адрес обновления карточки"""
        self._assert_url_resolves_to_views(
            name='resumes:fill_card',
            view_class=CardUpdateView,
            pk=1,
        )

    def test_card_detail_url(self):
        """Проверяем URL-адрес детального просмотра карточки"""
        self._assert_url_resolves_to_views(
            name='resumes:card_detail',
            view_class=CardDetailView,
            pk=1,
        )

    def test_advanced_search_cards_url(self):
        """Проверяем URL-адрес расширенного поиска карточек"""
        self._assert_url_resolves_to_views(
            name='resumes:advanced_search_cards',
            view_class=AdvancedCardSearchView,
        )

    def test_home_screen_search_url(self):
        """Проверяем URL-адрес поиска карточек на главном экране"""
        self._assert_url_resolves_to_views(
            name='resumes:home_screen_search',
            view_class=HomeScreenCardSearchView,
        )

    def test_file_delete_url(self):
        """Проверяем URL-адрес удаления файла"""
        self._assert_url_resolves_to_views(
            name='resumes:delete_file',
            view_class=FileDeleteView,
            pk=1,
        )

    def test_image_delete_url(self):
        """Проверяем URL-адрес удаления изображения"""
        self._assert_url_resolves_to_views(
            name='resumes:delete_image',
            view_class=ImageDeleteView,
            pk=1,
        )

    def test_resolve_card_update_invalid_pk_type(self):
        """Проверяем, что URL-адрес обновления карточки с недопустимым PK возвращает 404"""
        self._assert_url_raises_404(url='/card/invalid/fill/')

    def test_resolve_card_update_url_negative_pk(self):
        """Проверяем, что URL-адрес обновления карточки с отрицательным PK возвращает 404"""
        self._assert_url_raises_404(url='/card/-1/fill/')

    def test_resolve_trailing_slash_sensitivity(self):
        """Проверяем, что URL без слеша не разрешается (если у нас все URL с /)."""
        self._assert_url_raises_404(url='/card/1')

    def test_file_delete_with_large_pk(self):
        """Проверяем, что очень большой PK не приводит к ошибке при удалении файла."""
        large_pk = 999999999
        self._assert_url_resolves_to_views(
            name="resumes:delete_file",
            view_class=FileDeleteView,
            pk=large_pk,
        )
