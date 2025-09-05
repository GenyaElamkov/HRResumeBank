from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.utils.decorators import method_decorator
from django.views import View

from .models.entity import Entity


@method_decorator(login_required, name="dispatch")
class ResumeListView(View):
    """
    Список всех резюме (Entity)
    """
    def get(self, request):
        entities = Entity.objects.select_related("template", "created").all()
        return render(request, "resumes/resume_list.html", {"entities": entities})


@method_decorator(login_required, name="dispatch")
class ResumeDetailView(View):
    """
    Просмотр резюме по entity_id
    """
    def get(self, request, entity_id):
        entity = get_object_or_404(Entity, id=entity_id)
        resume_data = {}
        for d in entity.date_entitydate.select_related("field").all():
            field_name = d.field.title
            value = (
                d.value_text
                or d.value_number
                or d.value_date
                or d.value_boolean
                or d.value_email
                or d.value_images
                or (d.file.original_name if d.file else None)
            )
            resume_data[field_name] = value

        context = {"entity": entity, "resume_data": resume_data}
        return render(request, "resumes/resume_detail.html", context)


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
            "error_message": "Внутренняя ошибка сайта, вернитесь на главную страницу, отчёт об ошибке мы направим администрации сайта",
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
