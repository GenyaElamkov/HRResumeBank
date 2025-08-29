from django.db import models

from .role import Role
from .permission import Permission


class RolePermission(models.Model):
    """Связь Ролей и разрешений"""

    role = models.ForeignKey(
        Role,
        verbose_name="Роль",
        help_text="Выберите роль",
        on_delete=models.CASCADE,
        related_name="roles_permission",
    )
    permission = models.ForeignKey(
        Permission,
        verbose_name="Разрешение",
        help_text="Выберите разрешение",
        on_delete=models.CASCADE,
        related_name="permissions",
    )

    def __str__(self):
        return f"{self.role} - {self.permission}"

    class Meta:
        verbose_name = "Роль/Разрешение"
        verbose_name_plural = "Роли/Разрешении"
        