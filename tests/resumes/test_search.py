from django.http import HttpResponse
from django.test import RequestFactory

import pytest

from core.apps.resumes.service.search import BaseCardSearchView


class TestSearchView(BaseCardSearchView):
    def render_to_response(self, context):
        return HttpResponse('OK')

    def get_field_search(self, results, words):
        return list(results)


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def search_view(factory):
    return TestSearchView()


@pytest.mark.django_db
def test_search_get_empty_request(factory, search_view, custom_user):
    """Проверяем обработку GET-запроса к представлению поиска с пустыми параметрами."""
    request = factory.get(
        '/search/',
        data={
            "q": "",
            "template": "",
            "created": "",
            "page": "",
        },
    )
    request.user = custom_user

    response = search_view.get(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_get_request(factory, search_view, custom_user):
    """Тестирует обработку GET-запроса к представлению поиска с параметрами."""
    request = factory.get(
        '/search/',
        data={
            "q": "python developer",
            "template": "1",
            "created": "2",
            "page": "1",
        },
    )
    request.user = custom_user

    response = search_view.get(request)
    assert response.status_code == 200
