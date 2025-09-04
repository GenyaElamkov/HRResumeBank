from django.contrib import admin

from .models.entity import Entity
from .models.entity_date import EntityDate
from .models.log import Log
from .models.template import Template
from .models.template_field import TemplateField


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Шаблонами резюме/карточки"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(TemplateField)
class TemplateFieldAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Полями шаблона"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Записями резюме/Сущностями"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(EntityDate)
class EntityDateAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Значениями динамических полей"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Журналом действий"
        return super().changelist_view(request, extra_context=extra_context)
