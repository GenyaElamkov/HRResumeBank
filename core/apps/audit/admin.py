from django.contrib import admin

from easyaudit.admin import (
    CRUDEventAdmin,
    LoginEventAdmin,
)
from easyaudit.models import (
    CRUDEvent,
    LoginEvent,
)


# Отменяем стандартную регистрацию
admin.site.unregister(CRUDEvent)
admin.site.unregister(LoginEvent)


@admin.register(CRUDEvent)
class CustomCRUDEventAdmin(CRUDEventAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(LoginEvent)
class CustomLoginEventAdmin(LoginEventAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
