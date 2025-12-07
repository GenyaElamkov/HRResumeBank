import re
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.db.models import (
    Q,
    QuerySet,
)
from django.http import HttpRequest
from django.views import View

from core.apps.accounts.models import CustomUser
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template


class BaseCardSearchView(View):
    """Базовое представление поиска карточек с общей логикой"""

    ITEMS_PER_PAGE = 52

    def get(self, request: HttpRequest, *args, **kwargs) -> Any:
        """Обработка Get-запроса с поиском и филтрацией"""
        query, template_id, created_id, page = self._extract_request_params(request)

        results = self._get_base_queryset()
        templates, users = self._get_base_related_objects()

        results = self._apply_filters(results, template_id, created_id)

        # Поиск карточек по заданному запросу
        if query:
            result_search: list[Card] = self._search(query, results)
            if result_search:
                # Передаю список слов — words, для поиска по полям
                words = self._extract_search_words(query)
                self.get_field_search(result_search, words)
            paginated_data = self._paginate_results(result_search, page)
        else:
            paginated_data = self._paginate_results(results, page)

        context = self._build_context(
            paginated_data=paginated_data,
            templates=templates,
            users=users,
            query=query,
            template_id=template_id,
            created_id=created_id,
        )
        return self.render_to_response(context=context)

    def get_field_search(self, results: QuerySet, words: list):
        """Метод поиска по полям (должен быть реализован в подклассах)"""
        raise NotImplementedError("Подклассы должны реализовать этот метод")

    def render_to_response(self, context):
        """Метод рендеринга должен быть реализован в подклассах"""
        raise NotImplementedError("Подклассы должны реализовать этот метод")

    def _extract_request_params(self, request: HttpRequest) -> tuple:
        """Извлечение параметров из запросов"""
        query = request.GET.get("q", "").strip()
        template_id = request.GET.get("template")
        created_id = request.GET.get("created")
        page = request.GET.get('page', 1)
        return query, template_id, created_id, page

    def _get_base_queryset(self) -> QuerySet[Card]:
        """Получение базового набора карточек"""
        return Card.objects.all().select_related('template')

    def _get_base_related_objects(self) -> tuple[QuerySet[Template], QuerySet[CustomUser]]:
        """Получение базовых связанных объектов"""
        templates = Template.objects.all()
        users = CustomUser.objects.all()
        return templates, users

    def _apply_filters(
        self, queryset: QuerySet[Card], template_id: Optional[str],
        created_id: Optional[str],
    ) -> QuerySet[Card]:
        """Применение фильтров"""
        # Фильтрация по пользователям
        if created_id:
            queryset = queryset.filter(created_id=created_id)
        # Фильтрация по шаблонам
        if template_id:
            queryset = queryset.filter(template_id=template_id)
        return queryset

    def _extract_search_words(self, query: str) -> List[str]:
        """Извлечение слов для поиска из запроса"""
        return query.strip('"').strip().split()

    def _search(self, query: str, queryset: QuerySet[Card]) -> List[Card]:
        """Выполняет поиск карточек по заданному запросу"""
        if not query or not queryset.exists():
            return list(queryset)

        words = self._extract_search_words(query)

        if self._is_exact_search(query):
            return self._exact_search(' '.join(words), queryset)
        else:
            return self._not_exact_search(words, queryset)

    def _is_exact_search(self, query: str) -> bool:
        """Проверка, является ли запрос точным (в кавычках)"""
        return query.startswith('"') and query.endswith('"')

    def _exact_search(self, phrase: str, queryset: QuerySet[Card]) -> List[Card]:
        """Поиск карточек по точному совпадению запроса"""
        q_objects = Q(values__icontains=phrase)
        filtered_queryset: QuerySet = queryset.filter(q_objects).distinct()
        return [
            card for card in filtered_queryset
            if self._contains_whole_words(card, phrase)
        ]

    def _contains_whole_words(self, card: Card, phrase: str) -> bool:
        """Проверка, содержит ли карточка все слова из запроса как целые слова"""
        text_parts = self._extract_text_from_card(card)
        full_text = ' '.join(text_parts)
        # Проверяем, что запрос содержит только выбранное слово
        pattern = rf'\b{re.escape(phrase.lower())}\b'
        return bool(re.search(pattern, full_text))

    def _extract_text_from_card(self, card: Card) -> List[str]:
        """Извлечение текста из карточки"""
        text_parts = []
        if not card.values:
            return text_parts

        for value in card.values.values():
            if isinstance(value, list):
                text_parts.append(' '.join(str(item).lower() for item in value))
            else:
                text_parts.append(str(value).lower())
        return text_parts

    def _not_exact_search(self, words: list, queryset: QuerySet[Card]) -> QuerySet[Card]:
        """Поиск карточек по не точному совпадению запроса"""

        q_objects = Q()
        for word in words:
            q_objects &= Q(values__icontains=word)

        return queryset.filter(q_objects).distinct()

    def _paginate_results(
        self, results: QuerySet[Card] | List[Card],
        page: str | int,
    ) -> Dict[str, Any]:
        """Получение пагинатора"""
        paginator = Paginator(results, self.ITEMS_PER_PAGE)
        try:
            paginated_results = paginator.page(page)
        except PageNotAnInteger:
            paginated_results = paginator.page(1)
        except EmptyPage:
            paginated_results = paginator.page(paginator.num_pages)

        return {
            "paginator": paginator,
            "paginated_results": paginated_results,
            "is_paginated": paginator.num_pages > 1,
        }

    def _build_context(
        self, paginated_data: Dict[str, Any],
        templates: QuerySet[Template],
        users: QuerySet[CustomUser],
        query: str,
        template_id: QuerySet[str],
        created_id: Optional[str],
    ) -> Dict[str, Any]:
        """Сборка контекста для шаблона"""
        return {
            "results": paginated_data["paginated_results"],
            "query": query,
            "template_id": template_id,
            "user_id": created_id,
            "templates": templates,
            "users": users,
            "paginator": paginated_data["paginator"],
            "page_obj": paginated_data["paginated_results"],
            "is_paginated": paginated_data["is_paginated"],
        }
