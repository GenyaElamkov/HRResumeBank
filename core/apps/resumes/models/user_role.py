from django.contrib.auth.models import User
from django.db import models

from .department import Department
from .role import Role


class UserRole(models.Model):
    """Связь Пользователя и Роли"""
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        on_delete=models.CASCADE,
        related_name="users",
    )
    role = models.ForeignKey(
        Role,
        verbose_name="Назначенная роль",
        help_text="Выберите роль",
        on_delete=models.CASCADE,
        related_name="roles",
    )
    department = models.ForeignKey(
        Department,
        verbose_name="Ограничение роли в рамка подразделения",
        help_text="Выберите подразделение",
        on_delete=models.CASCADE,
        related_name="user_roles",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user}: {self.role}, {self.department}"

    class Meta:
        verbose_name = "Пользователь/Роль"
        verbose_name_plural = "Пользователи/Роли"

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                condition=models.Q(department__isnull=True),
                name='unique_user_role_department',
            ),
            models.UniqueConstraint(
                fields=['user', 'role'],
                condition=models.Q(department__isnull=False),
                name='unique_user_role_with_department',
            ),
        ]
        indexes = [
            models.Index(fields=['user', 'role']),
        ]
