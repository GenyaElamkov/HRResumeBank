from django.db import models

from .team import Team
from .department import Department


class DepartmentGroup(models.Model):
    """Модель связывающая Департамент и Группу"""
    group = models.ForeignKey(
        Team,
        verbose_name="Группа",
        help_text="Выберите группу",
        on_delete=models.CASCADE,
        related_name="department_links",
    )
    department = models.ForeignKey(
        Department,
        verbose_name="Принадлежность группы к подразделению",
        help_text="Выберите подразделение",
        on_delete=models.CASCADE,
        related_name="group_links",
    )

    def __str__(self):
        return f"{self.department}: {self.group}"

    class Meta:
        verbose_name = "Департамент/Группа"
        verbose_name_plural = "Департаменты/Группы"