from enum import StrEnum

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Group,
    Permission,
)
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate


class UserPerm(StrEnum):
    """Разрешения пользователей"""
    ADD = 'add_customuser'
    CHANGE = 'change_customuser'
    DELETE = 'delete_customuser'
    VIEW = 'view_customuser'


class TemplatePerm(StrEnum):
    """Разрешения на шаблоны в модели Template"""
    ADD = 'add_template'
    CHANGE = 'change_template'
    DELETE = 'delete_template'
    VIEW = 'view_template'


class TemplateFieldPerm(StrEnum):
    """Разрешение на динамические поля модели EntityData"""
    ADD = 'add_templatefield'
    CHANGE = 'change_templatefield'
    DELETE = 'delete_template_field'
    VIEW = 'view_template_field'


class CardPerm(StrEnum):
    """Разрешения в резуюме/сущность модели Entity"""
    ADD = 'add_card'
    CHANGE = 'change_card'
    DELETE = 'delete_card'
    VIEW = 'view_card'


def create_default_groups(sender, **kwargs):
    """Создает группы по умолчанию"""

    user = get_user_model()
    ContentType.objects.get_for_model(user)

    groups_permissions = {
        "Администратор": [
            UserPerm.ADD,
            UserPerm.CHANGE,
            UserPerm.DELETE,
            UserPerm.VIEW,
            TemplatePerm.ADD,
            TemplatePerm.CHANGE,
            TemplatePerm.DELETE,
            TemplatePerm.VIEW,
            TemplateFieldPerm.ADD,
            TemplateFieldPerm.CHANGE,
            TemplateFieldPerm.DELETE,
            TemplateFieldPerm.VIEW,
            CardPerm.ADD,
            CardPerm.CHANGE,
            CardPerm.DELETE,
            CardPerm.VIEW,
        ],
        "Редактор": [
            CardPerm.ADD,
            CardPerm.CHANGE,
            CardPerm.VIEW,

        ],
        "Читатель": [
            CardPerm.VIEW,
        ],
    }

    for group_name, perm_codes in groups_permissions.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(
            codename__in=perm_codes,
        )
        group.permissions.set(permissions)
        group.save()


post_migrate.connect(create_default_groups)
