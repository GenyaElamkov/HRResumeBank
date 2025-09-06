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


class EntityPerm(StrEnum):
    """Разрешения в резуюме/сущность модели Entity"""
    ADD = 'add_entity'
    CHANGE = 'change_entity'
    DELETE = 'delete_entitydata'
    VIEW = 'view_entitydata'


class EntityDataPerm(StrEnum):
    """Разрешение на динамические поля модели EntityData"""
    ADD = 'add_entity_data'
    CHANGE = 'change_entity_data'
    DELETE = 'delete_entity_data'
    VIEW = 'view_entity_data'


def create_default_groups(sender, **kwargs):
    """Создает группы по умолчанию"""

    groups_permissions = {
        "Администратор": [
            UserPerm.ADD, UserPerm.CHANGE,
            UserPerm.DELETE, UserPerm.VIEW,
            EntityPerm.ADD, EntityPerm.CHANGE,
            EntityPerm.VIEW, EntityPerm.DELETE,
            EntityDataPerm.ADD, EntityDataPerm.CHANGE,
            EntityDataPerm.VIEW, EntityDataPerm.DELETE,
        ],
        "Редактор": [
            EntityPerm.ADD, EntityPerm.CHANGE, EntityPerm.VIEW,
            EntityDataPerm.ADD, EntityDataPerm.CHANGE, EntityDataPerm.VIEW,
        ],
        "Читатель": [
            EntityPerm.VIEW, EntityDataPerm.VIEW,
        ],
    }

    user = get_user_model()
    ContentType.objects.get_for_model(user)

    for group_name, perm_codes in groups_permissions.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        permissions = Permission.objects.filter(
            codename__in=perm_codes,
        )
        group.permissions.set(permissions)
        group.save()


post_migrate.connect(create_default_groups)
