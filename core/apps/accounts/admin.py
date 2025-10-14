from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "get_full_name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация",
            {"fields": ("last_name", "first_name", "surname", "email")},
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

    def get_form(self, request, obj=None, **kwargs):
        """Скрываем поля is_superuser, is_staff для обычных пользователей"""
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].widget = forms.HiddenInput()

            if 'is_staff' in form.base_fields:
                form.base_fields['is_staff'].widget = forms.HiddenInput()

        return form

    def get_queryset(self, request):
        """Скрываем superuser для обычных пользователей"""
        if not request.user.is_superuser:
            return super().get_queryset(request).filter(is_superuser=False)
        return super().get_queryset(request)
