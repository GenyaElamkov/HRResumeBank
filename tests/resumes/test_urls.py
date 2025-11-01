from django.test import TestCase
from django.urls import (
    NoReverseMatch,
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

    def test_card_list_url(self):
        """Проверяем URL-адрес списка карточек"""
        url = reverse('resumes:card_list')
        self.assertEqual(url, '/')
        resolved = resolve('/')
        self.assertEqual(resolved.func.view_class, CardListView)

    def test_card_create_url(self):
        """Проверяем URL-адрес создания карточки"""
        url = reverse('resumes:create_card')
        self.assertEqual(url, '/card/create/')
        resolved = resolve('/card/create/')
        self.assertEqual(resolved.func.view_class, CardCreateView)

    def test_card_update_url(self):
        """Проверяем URL-адрес обновления карточки"""
        url = reverse('resumes:fill_card', kwargs={'pk': 1})
        self.assertEqual(url, '/card/1/fill/')
        resolved = resolve('/card/1/fill/')
        self.assertEqual(resolved.func.view_class, CardUpdateView)

    def test_card_detail_url(self):
        """Проверяем URL-адрес детального просмотра карточки"""
        url = reverse('resumes:card_detail', kwargs={'pk': 1})
        self.assertEqual(url, '/card/1/')
        resolved = resolve('/card/1/')
        self.assertEqual(resolved.func.view_class, CardDetailView)

    def test_advanced_search_cards_url(self):
        """Проверяем URL-адрес расширенного поиска карточек"""
        url = reverse('resumes:advanced_search_cards')
        self.assertEqual(url, '/cards/advanced-search/')
        resolved = resolve('/cards/advanced-search/')
        self.assertEqual(resolved.func.view_class, AdvancedCardSearchView)

    def test_home_screen_search_url(self):
        """Проверяем URL-адрес поиска карточек на главном экране"""
        url = reverse('resumes:home_screen_search')
        self.assertEqual(url, '/cards/home-screen/')
        resolved = resolve('/cards/home-screen/')
        self.assertEqual(resolved.func.view_class, HomeScreenCardSearchView)

    def test_file_delete_url(self):
        """Проверяем URL-адрес удаления файла"""
        url = reverse('resumes:delete_file', kwargs={'pk': 1})
        self.assertEqual(url, '/card/file/1/delete/')
        resolved = resolve('/card/file/1/delete/')
        self.assertEqual(resolved.func.view_class, FileDeleteView)

    def test_image_delete_url(self):
        """Проверяем URL-адрес удаления изображения"""
        url = reverse('resumes:delete_image', kwargs={'pk': 1})
        self.assertEqual(url, '/card/image/1/delete/')
        resolved = resolve('/card/image/1/delete/')
        self.assertEqual(resolved.func.view_class, ImageDeleteView)

    def test_card_update_invalid_pk_type(self):
        """Проверяем, что URL-адрес обновления карточки с недопустимым PK возвращает 404"""
        with self.assertRaises(Resolver404):
            resolve('/card/invalid/fill/')

    def test_card_update_url_negative_pk(self):
        """Проверяем, что URL-адрес обновления карточки с отрицательным PK возвращает 404"""
        with self.assertRaises(Resolver404):
            resolve('/card/-1/fill/')

    def test_reverse_non_existent_name(self):
        """Проверяем, попытка обратиться к несуществующему имени вызывает исключение"""
        with self.assertRaises(NoReverseMatch):
            reverse('resumes:non_existent_name')

    def test_trailing_slash_sensitivity(self):
        """Проверяем, что URL без слеша не разрешается (если у нас все URL с /)."""
        with self.assertRaises(Resolver404):
            resolve('/card/1')

    def test_file_delete_with_large_pk(self):
        """Проверяем, что очень большой PK не приводит к ошибке при удалении файла."""
        large_pk = 999999999
        url = reverse("resumes:delete_file", kwargs={"pk": large_pk})
        self.assertEqual(url, f"/card/file/{large_pk}/delete/")
        resolved = resolve(url)
        self.assertEqual(resolved.func.view_class, FileDeleteView)
