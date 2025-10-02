from django.contrib import admin

from .models.card import Card
from .models.log import Log
from .models.template import Template
from .models.template_field import TemplateField


class TemplateFieldInline(admin.StackedInline):
    model = TemplateField
    extra = 0


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateFieldInline]

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Шаблонами резюме/карточки"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['main_name', 'id', 'template', 'create_at', 'update_at']
    list_filter = ('create_at', 'update_at')
    search_fields = ['id', 'main_name']
    ordering = ['create_at', 'update_at']

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Карточками"
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Журналом действий"
        return super().changelist_view(request, extra_context=extra_context)
