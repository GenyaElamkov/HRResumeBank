import os

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
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


class PermissionComposer:
    """Права доступа для контекста"""
    @staticmethod
    def get_context_data(context, user):
        context['is_admin_or_superuser'] = PermissionComposer.check_permission(user=user, permissions=['Администратор'])
        context['can_edit'] = PermissionComposer.check_permission(user=user, permissions=["Администратор", "Редактор"])
        return context

    @staticmethod
    def check_permission(user, permissions: list):
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=permissions).exists()


class EditorRequiredMixin(UserPassesTestMixin):
    """Права доступа для Редактора, Администратора и superuser"""
    def test_func(self):
        """Проверка, что пользователь является Администратором, Редактором и superuser"""
        return (
            self.request.user.groups.filter(name__in=["Администратор", "Редактор"]).exists()
            or self.request.user.is_superuser
        )


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

        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )

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

        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )

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
        if images.exists():
            context['images'] = images
        else:
            context['images'] = None


class CardCreateView(EditorRequiredMixin, CreateView):
    """Создать карточку"""
    form_class = CardCreateForm
    template_name = "resumes/create_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['created'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse("resumes:update_card", kwargs={"pk": self.object.pk})


class CardUpdateView(EditorRequiredMixin, UpdateView):
    """Обновление карточки"""
    model = Card
    form_class = CardFillForm
    template_name = "resumes/update_card.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )

        card = self.object
        images = ProfileImage.objects.filter(card=card).order_by("create_at")

        self._add_files_to_context(context, card)
        context['card_images'] = images

        return context

    def _add_files_to_context(self, context, card):
        files = FileStorage.objects.filter(card=card)
        if files.exists():
            files_with_names = []
            for file in files:
                file_name = os.path.basename(file.uploaded_file.name)
                files_with_names.append((file, file_name))
            context['files'] = files_with_names
        else:
            context['files'] = None

    def get_success_url(self):
        return reverse("resumes:card_detail", kwargs={"pk": self.object.pk})


class FileDeleteView(DeleteView):
    """Удаление файлов"""
    model = FileStorage
    template_name = "resumes/partials/confirm_file_delete.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )
        return context

    def get_success_url(self):
        return reverse(
            "resumes:update_card", kwargs={"pk": self.object.card.pk},
        )


class ImageDeleteView(DeleteView):
    """Удаление изображений"""
    model = ProfileImage
    template_name = "resumes/partials/confirm_image_delete.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )
        return context

    def get_success_url(self):
        return reverse(
            "resumes:update_card", kwargs={"pk": self.object.card.pk},
        )


class AdvancedCardSearchView(BaseCardSearchView):
    """Представление расширенного поиска карточек"""

    def get_field_search(self, results_query, words: list) -> list:
        """Получает поля, значения поиска с оптимизацией"""
        exact = False
        query = self.request.GET.get('q', '').strip()
        if query.startswith('"') and query.endswith('"'):
            query_text = " ".join(words).lower()
            exact = True

        cards_with_matches = []
        for card in results_query:
            matched_fields = {}
            for field_name, field_value in card.values.items():
                value_str = ""
                if isinstance(field_value, str):
                    value_str = field_value
                elif isinstance(field_value, (int, float)):
                    value_str = str(field_value)
                elif isinstance(field_value, list):
                    value_str = ' '.join(str(item) for item in field_value)
                else:
                    value_str = str(field_value)

                if exact and query_text in value_str.lower():
                    matched_fields[field_name] = value_str
                elif any(word.lower() in value_str.lower() for word in words):
                    matched_fields[field_name] = value_str

            # Если есть совпадения в полях, создаем поле matched_fields и добавляем карточку
            if matched_fields:
                card.matched_fields = matched_fields
            cards_with_matches.append(card)
        return cards_with_matches

    def render_to_response(self, context):
        """Рендеринг с использованием шаблона advanced_search.html"""
        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )
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

        context.update(
            PermissionComposer.get_context_data(
                context=context,
                user=self.request.user,
            ),
        )

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
