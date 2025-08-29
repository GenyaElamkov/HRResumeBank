from django.contrib.auth.models import User
from django.db import models

from .team import Team


class UserGroup(models.Model):
    """Модель связывающая Пользователя и Группу"""

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
        on_delete=models.CASCADE,
        related_name="user_group",
    )
    group = models.ForeignKey(
        Team,
        verbose_name="Группа",
        help_text="Выберите группу",
        on_delete=models.CASCADE,
        related_name="groups",
    )

    def __str__(self):
        return f"{self.user}: {self.group}"

    class Meta:
        verbose_name = "Пользователь/Группа"
        verbose_name_plural = "Пользователи/Группы"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'group'],
                name='unique_user_group',
            ),
        ]
