from django.db import models
from django.contrib.auth.models import User

from .department import Department
from core.apps.common.models import TimeBaseModel


class Staff(TimeBaseModel):
    """Кастомная модель User"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь системы",
        help_text="Выберите пользователя",
        related_name="employee_profile",
    )
    department = models.ForeignKey(
        Department,
        verbose_name="Депортамент/Отдел",
        help_text="Выберите подразделение",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users"
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Персонал"

    def __str__(self):
        return self.user.username
