from django.contrib import admin

from .models.department import Department
from .models.department_group import DepartmentGroup
from .models.permission import Permission
from .models.role import Role
from .models.role_permission import RolePermission
from .models.staff import Staff
from .models.team import Team
from .models.user_role import UserRole
from .models.user_group import UserGroup


@admin.register(Department)
class DeportmentAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Департаментом/Отделом"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Персоналом"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Ролями"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление связми Пользователя и Роли"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Разрешениями"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление связями Ролями/Разрешениями"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Группами"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(DepartmentGroup)
class DepartmentGroupAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Департаментами/Группами"
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        extra_context['title'] = "Управление Пользователь/Группа"
        return super().changelist_view(request, extra_context=extra_context)
