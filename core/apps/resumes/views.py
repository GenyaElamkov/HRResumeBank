from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from core.apps.accounts.models import CustomUser

from .forms import (
    CardCreateForm,
    CardFillForm,
)
from .models.card import Card
from .models.template import Template


class CardListView(ListView):
    """Список карточек"""
    template_name = "resumes/card_list.html"
    context_object_name = "entities"
    paginate_by = 20
    allow_empty = True

    def get_queryset(self):
        return Card.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if request.headers.get('HX-Request'):
            return render(request, 'resumes/partials/card_list_content.html', context)

        return self.render_to_response(context)


class CardCreateView(CreateView):
    """Создать карточку"""
    ...


class CartDetailView(DetailView):
    """Показать документ по pk"""
    model = Card
    template_name = "resumes/card_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("template", "created")


def create_card(request):
    if request.method == "POST":
        form = CardCreateForm(request.POST, created=request.user)
        if form.is_valid():
            card = form.save()
            return redirect("resumes:fill_card", card_id=card.id)
    else:
        form = CardCreateForm(created=request.user)
    return render(request, "resumes/create_card.html", {"form": form})


def fill_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, created=request.user)
    if request.method == "POST":
        form = CardFillForm(card, request.POST)
        if form.is_valid():
            form.save()
            return redirect("resumes:card_detail", card_id=card.id)
    else:
        form = CardFillForm(card)
    return render(request, "resumes/fill_card.html", {"form": form, "card": card})


def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id, created=request.user)
    return render(request, "resumes/card_detail.html", {"card": card})


def advanced_search_cards(request):
    query = request.GET.get("q", "").strip()
    template_id = request.GET.get("template")
    user_id = request.GET.get("created")

    results = Card.objects.all()

    if user_id:
        results = results.filter(user_id=user_id)

    if template_id:
        results = results.filter(template_id=template_id)

    if query:
        words = query.split()
        q_objects = Q()
        for word in words:
            q_objects &= Q(values__icontains=word)
        results = results.filter(q_objects)

    templates = Template.objects.all()
    print(templates)
    users = CustomUser.objects.all()

    return render(
        request, "resumes/advanced_search.html", {
            "results": results,
            "query": query,
            "template_id": template_id,
            "user_id": user_id,
            "templates": templates,
            "users": users,
        },
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
