from django.shortcuts import render
from django.views.generic import (
    DetailView,
    ListView,
)

from .models.entity import Entity
from .models.template import Template


# @method_decorator(login_required, name="dispatch")
class ResumeListView(ListView):
    """Список всех резюме (Entity)"""
    template_name = "resumes/resume_list.html"
    context_object_name = "entities"
    paginate_by = 20
    allow_empty = True

    def get_queryset(self):
        return (
            Entity.objects
            .select_related("template", "created")
            .order_by("-create_at").all()
        )


class ResumeDetailView(DetailView):
    """Резюме по pk"""
    model = Entity
    template_name = "resumes/resume_detail.html"
    context_object_name = "entity"

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("template", "created")
            .prefetch_related("date_entitydate__field")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entity = self.object

        entity_data = entity.date_entitydate.all()

        primary_field = entity_data.filter(field__is_primary=True).first()
        if primary_field:
            entity.main_name = getattr(primary_field, f'value_{primary_field.field.type_field}', 'Резюме')

        context['entity_data'] = entity_data
        return context


class TemplateListView(ListView):
    """Список всех шаблонов (Temlate)"""
    template_name = "resumes/template_list.html"
    context_object_name = "templates"
    paginate_by = 9
    allow_empty = True

    def get_queryset(self):
        return (
            Template.objects
            .select_related("created")
            .order_by("-create_at").all()
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
