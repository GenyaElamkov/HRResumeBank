import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from core.apps.resumes.service.search import BaseCardSearchView

from .forms import (
    CardCreateForm,
    CardFillForm,
)
from .models.card import Card
from .models.file_storage import FileStorage
from .models.profile_image import ProfileImage


class CardListView(ListView):
    """Список карточек"""
    template_name = "resumes/card_list.html"
    context_object_name = "card_list"
    paginate_by = 52
    allow_empty = True

    def get_queryset(self):
        return Card.objects.all().select_related('template')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Преобразуем данные для шаблона
        cards = []
        for card in context["card_list"]:
            cards.append({
                "card": card,
                "values": {
                    field.title: card.values.get(field.title, "")
                    for field in card.template.fields.all()
                },
                "image": ProfileImage.objects.filter(card=card).first(),
            })

        context["card_list"] = cards
        context["query"] = self.request.GET.get('q', '')
        return context


class CardDetailView(DetailView):
    """Показать документ по pk"""
    model = Card
    template_name = "resumes/card_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("template", "created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        card = self.object

        self._add_files_to_context(context, card)
        self._add_images_to_context(context, card)
        return context

    def _add_files_to_context(self, context, card):
        files = FileStorage.objects.filter(card=card)
        if files.exists():
            files_name = [os.path.basename(file.uploaded_file.name) for file in files]
            context['files'] = zip(files, files_name)
        else:
            context['files'] = None

    def _add_images_to_context(self, context, card):
        images = ProfileImage.objects.filter(card=card)
        images = ProfileImage.objects.filter(card=card)
        if images.exists():
            context['images'] = images
        else:
            context['images'] = None


class CardCreateView(LoginRequiredMixin, CreateView):
    """Создать карточку"""
    form_class = CardCreateForm
    template_name = "resumes/create_card.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['created'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("resumes:fill_card", kwargs={"pk": self.object.pk})


class CardUpdateView(UpdateView):
    """Обновление карточки"""
    model = Card
    form_class = CardFillForm
    template_name = "resumes/fill_card.html"

    def get_success_url(self):
        return reverse("resumes:card_detail", kwargs={"pk": self.object.pk})


class AdvancedCardSearchView(BaseCardSearchView):
    """Представление расширенного поиска карточек"""

    def get_field_search(self, results_query, words: list) -> list:
        """Получает поля, значения поиска с оптимизацией"""
        cards_with_matches = []

        for card in results_query:
            matched_fields = {}
            for field_name, field_value in card.values.items():
                if isinstance(field_value, str) and any(word.lower() in field_value.lower() for word in words):
                    matched_fields[field_name] = field_value
                elif isinstance(field_value, (int, float)) and any(str(word) in str(field_value) for word in words):
                    matched_fields[field_name] = str(field_value)
                elif isinstance(field_value, list):
                    for item in field_value:
                        if isinstance(item, str) and any(word.lower() in item.lower() for word in words):
                            matched_fields[field_name] = str(field_value)
                            break

            if matched_fields:
                card.matched_fields = matched_fields
                cards_with_matches.append(card)

        return cards_with_matches

    def render_to_response(self, context):
        """Рендеринг с использованием шаблона advanced_search.html"""
        return render(
            self.request,
            "resumes/advanced_search.html",
            context,
        )


class HomeScreenCardSearchView(BaseCardSearchView):
    """Представление поиска карточек на основном экране"""

    def get_field_search(self, results_query, words: list) -> list:
        """Упрощенный поиск по ключевым словам"""
        matching_cards = []

        for card in results_query:
            card_values = ' '.join(str(value) for value in card.values.values()).lower()

            if any(word.lower() in card_values for word in words):
                matching_cards.append(card)

        return matching_cards

    def render_to_response(self, context):
        """Рендеринг с использованием шаблона card_list.html"""
        card_list = []
        for card in context['results']:
            card_list.append({
                "card": card,
                "values": {
                    field.title: card.values.get(field.title, "")
                    for field in card.template.fields.all()
                },
                "image": ProfileImage.objects.filter(card=card).first(),
            })

        context["card_list"] = card_list
        if self.request.headers.get('HX-Request'):
            # HTMX запрос - возвращаем только контент
            return render(
                self.request,
                "resumes/partials/card_list_content.html",
                context,
            )
        else:
            # Обычный запрос - возвращаем полную страницу
            return render(
                self.request,
                "resumes/card_list.html",
                context,
            )


def tr_handler404(request, exception):
    """Обработка ошибки 404"""
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=404,
        context={
            "title": "Страница не найдена: 404",
            "error_message": "К сожалению такая страница была не найдена, или перемещена",
            "error_top_message": "Страница не найдена",
            "status": "404",
        },
    )


def tr_handler500(request):
    """Обработка ошибки 500"""
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=500,
        context={
            "title": "Ошибка сервера: 500",
            "error_message": "Внутренняя ошибка сайта, вернитесь на главную страницу, \
                отчёт об ошибке мы направим администрации сайта",
            "error_top_message": "Ошибка сервера",
            "status": "500",
        },
    )


def tr_handler403(request, exception):
    """Обработка ошибки 403"""
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=403,
        context={
            "title": "Ошибка доступа: 403",
            "error_message": "Доступ к этой странице ограничен",
            "error_top_message": "Ошибка доступа",
            "status": "403",
        },
    )
