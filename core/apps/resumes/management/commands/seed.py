from random import (  # noqa
    choice,
    randint,
    randrange,
)

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from faker import Faker

from core.apps.resumes.models.entity import Entity
from core.apps.resumes.models.entity_date import EntityDate
from core.apps.resumes.models.log import Log
from core.apps.resumes.models.template import Template
from core.apps.resumes.models.template_field import TemplateField


class Command(BaseCommand):
    """Заполняет базу тестовыми данными (seed)"""

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== Очищаем старые данные ==="))

        User = get_user_model()

        Template.objects.all().delete()
        TemplateField.objects.all().delete()
        EntityDate.objects.all().delete()
        Entity.objects.all().delete()
        Log.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS("Данные очищены!"))

        fake = Faker("ru_RU")

        # --- Пользователи ---
        user1, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_superuser": True, "is_staff": True},
        )
        user2, _ = User.objects.get_or_create(username="sanya")
        user3, _ = User.objects.get_or_create(username="genya")
        user4, _ = User.objects.get_or_create(username="vasilek")

        # --- Шаблоны ---
        template, _ = Template.objects.get_or_create(title="Резюме")
        template_organization, _ = Template.objects.get_or_create(title="Организация")

        # --- Поля шаблона ---
        field_name, _ = TemplateField.objects.get_or_create(
            template=template,
            title="ФИО",
            type_field=TemplateField.TypeField.TEXT,
            is_required=True,
            is_primary=True,
            order=1,
        )
        field_birth, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Дата рождения",
            type_field=TemplateField.TypeField.DATE,
            order=2,
        )
        field_experience, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Опыт (лет)",
            type_field=TemplateField.TypeField.NUMBER,
            order=3,
        )
        field_email, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Email",
            type_field=TemplateField.TypeField.EMAIL,
            order=4,
        )
        field_images, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Фотография",
            type_field=TemplateField.TypeField.IMAGE,
            order=5,
        )
        # Поля шаблона организации
        field_name_organization, _ = TemplateField.objects.get_or_create(
            template=template_organization,
            title="ИНН",
            type_field=TemplateField.TypeField.TEXT,
            is_required=True,
            is_primary=True,
            order=1,
        )

        # --- Генерация 100 записей ---
        for i in range(100):
            created_user = choice([user1, user2, user3, user4])

            entity = Entity.objects.create(
                template=template,
                created=created_user,
            )

            # Значения
            EntityDate.objects.create(
                entity=entity,
                field=field_name,
                value_text=fake.name(),
            )
            EntityDate.objects.create(
                entity=entity,
                field=field_birth,
                value_date=fake.date_of_birth(minimum_age=18, maximum_age=60),
            )
            EntityDate.objects.create(
                entity=entity,
                field=field_experience,
                value_number=randint(0, 30),
            )
            EntityDate.objects.create(
                entity=entity,
                field=field_email,
                value_email=fake.email(),
            )
            EntityDate.objects.create(
                entity=entity,
                field=field_images,
                value_images=fake.image_url(),
            )

            # Лог действия
            Log.objects.create(
                user=created_user,
                action="Создание резюме",
                details=f"Создано резюме {entity.id}",
            )

            inn = randrange(1000, 26444546)
            entity_organization = Entity.objects.create(
                template=template_organization,
                created=created_user,
            )
            # Значение для организации
            EntityDate.objects.create(
                entity=entity_organization,
                field=field_name_organization,
                value_number=inn,
            )
            # Лог действия для организации
            Log.objects.create(
                user=created_user,
                action="Создание организации",
                details=f"Создана организация {entity_organization.id}",
            )

        self.stdout.write(self.style.SUCCESS("✅ Создано 100 резюме"))
