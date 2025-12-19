from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models.card import Card
from .models.template import Template
from .models.template_field import TemplateField


class TemplateFieldAdminForm(forms.ModelForm):
    class Meta:
        model = TemplateField
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['title'].help_text = mark_safe(
                '<span style="color: #d4ac0d; font-weight: bold; font-size: 0.9em; display: block; margin-top: 4px;">'
                '⚠️ Внимание: Изменение имени поля может привести к потере связи со старыми значениями '
                'в карточках.'
                '</span>',
            )


class TemplateFieldInline(admin.StackedInline):
    model = TemplateField
    form = TemplateFieldAdminForm
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
