import re

from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.db.models import (
    Q,
    QuerySet,
)
from django.views import View

from core.apps.accounts.models import CustomUser
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template


class BaseCardSearchView(View):
    """Базовое представление поиска карточек с общей логикой"""

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        template_id = request.GET.get("template")
        created_id = request.GET.get("created")
        page = request.GET.get('page', 1)

        results = Card.objects.all().select_related('template')
        templates = Template.objects.all()
        users = CustomUser.objects.all()

        # Фильтрация по пользователям
        if created_id:
            results = results.filter(created_id=created_id)

        # Фильтрация по шаблонам
        if template_id:
            results = results.filter(template_id=template_id)

        # Поиск карточек по заданному запросу
        if not query:
            paginator = self._get_paginator(results, page)
        else:
            result_search: list[Card] = self._search(query, results)
            # Передаю список слов — words, для поиска по полям
            words = query.strip('"').strip().split()
            self.get_field_search(result_search, words)
            paginator = self._get_paginator(result_search, page)

        context = self._get_context(
            paginator=paginator['paginator'],
            paginated_results=paginator['paginated_results'],
            templates=templates,
            users=users,
            query=query,
            template_id=template_id,
            created_id=created_id,
        )
        return self.render_to_response(context=context)

    def get_field_search(self, results: QuerySet, words: list):
        """Метод поиска по полям (должен быть реализован в подклассах)"""
        raise NotImplementedError("Subclasses must implement this method")

    def render_to_response(self, context):
        """Метод рендеринга должен быть реализован в подклассах"""
        raise NotImplementedError("Subclasses must implement this method")

    def _search(self, query: str, results: QuerySet[Card]) -> list[Card]:
        """Выполняет поиск карточек по заданному запросу"""
        if not query:
            return results

        words = query.strip('"').strip().split()
        if query.startswith('"') and query.endswith('"'):
            phrase = ' '.join(words)
            results_filter = self._exact_search(phrase=phrase, results=results)
        else:
            results_filter = self._not_exact_search(words=words, results=results)

        return results_filter

    def _exact_search(self, phrase: str, results: QuerySet[Card]) -> list[Card]:
        """Поиск карточек по точному совпадению запроса"""
        q_objects = Q(values__icontains=phrase)
        results_filter_start: QuerySet = results.filter(q_objects).distinct()
        return [
            card for card in results_filter_start
            if self._contains_whole_words(card, phrase)
        ]

    def _contains_whole_words(self, card: Card, phrase: str):
        """Проверка, содержит ли карточка все слова из запроса"""
        text_parts = []
        for value in card.values.values():
            if isinstance(value, list):
                text_parts.append(' '.join(str(item).lower() for item in value))
            else:
                text_parts.append(str(value).lower())

        full_text = ' '.join(text_parts)
        # Проверяем, что запрос содержит только выбранное слово
        pattern = rf'\b{re.escape(phrase.lower())}\b'
        return re.search(pattern, full_text) is not None

    def _not_exact_search(self, words: list, results: QuerySet[Card]) -> list[Card]:
        """Поиск карточек по не точному совпадению запроса"""
        q_objects = Q()
        for word in words:
            q_objects &= Q(values__icontains=word)

        return results.filter(q_objects).distinct()

    def _get_paginator(self, cards_matches: QuerySet[Card], page) -> dict:
        """Получение пагинатора"""
        paginator = Paginator(cards_matches, 52)
        try:
            paginated_results = paginator.page(page)
        except PageNotAnInteger:
            paginated_results = paginator.page(1)
        except EmptyPage:
            paginated_results = paginator.page(paginator.num_pages)

        return {
            "paginator": paginator,
            "paginated_results": paginated_results,
        }

    def _get_context(self, paginator, paginated_results, templates, users, query, template_id, created_id):
        """Получение контекста"""
        return {
            "results": paginated_results,
            "query": query,
            "template_id": template_id,
            "user_id": created_id,
            "templates": templates,
            "users": users,
            "paginator": paginator,
            "page_obj": paginated_results,
            "is_paginated": paginator.num_pages > 1,
        }
