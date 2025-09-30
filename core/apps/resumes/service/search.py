from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator,
)
from django.db.models import Q
from django.views import View

from core.apps.accounts.models import CustomUser
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template


class BaseCardSearchView(View):
    """Базовое представление поиска карточек с общей логикой"""

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        template_id = request.GET.get("template")
        user_id = request.GET.get("created")
        page = request.GET.get('page', 1)

        results = Card.objects.all().select_related('template')
        cards_matches = []

        # Фильтрация по пользователям
        if user_id:
            results = results.filter(user_id=user_id)

        # Фильтрация по шаблонам
        if template_id:
            results = results.filter(template_id=template_id)

        # Поиск по ключевым словам
        if query:
            words = query.split()
            q_objects = Q()

            # Если | в поисковой строке, то поиск по OR
            # Если & в поисковой строке, то поиск по AND
            for word in words:
                q_objects &= Q(values__icontains=word)

            results = results.filter(q_objects).distinct()
            cards_matches = self.get_field_search(results, words)
        else:
            cards_matches = list(results)

        # Пагинация
        paginator = Paginator(cards_matches, 52)
        try:
            paginated_results = paginator.page(page)
        except PageNotAnInteger:
            paginated_results = paginator.page(1)
        except EmptyPage:
            paginated_results = paginator.page(paginator.num_pages)

        # Дополнительные данные для контекста
        templates = Template.objects.all()
        users = CustomUser.objects.all()

        context = {
            "results": paginated_results,
            "query": query,
            "template_id": template_id,
            "user_id": user_id,
            "templates": templates,
            "users": users,
            "paginator": paginator,
            "page_obj": paginated_results,
            "is_paginated": paginator.num_pages > 1,
        }
        return self.render_to_response(context=context)

    def get_field_search(self, results, words):
        """Метод поиска по полям (должен быть реализован в подклассах)"""
        return list(results)

    def render_to_response(self, context):
        """Метод рендеринга должен быть реализован в подклассах"""
        raise NotImplementedError("Subclasses must implement this method")
