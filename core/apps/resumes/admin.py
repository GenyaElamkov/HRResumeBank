from django.contrib import admin

from .models.department import Department


from .models.staff import Staff


@admin.register(Department)
class DeportmentAdmin(admin.ModelAdmin):
    ...


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    ...