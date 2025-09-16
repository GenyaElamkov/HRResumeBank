import sys
from random import (  # noqa
    choice,
    randint,
    randrange,
)

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from faker import Faker

from core.apps.resumes.models.card import Card
from core.apps.resumes.models.log import Log
from core.apps.resumes.models.template import Template
from core.apps.resumes.models.template_field import TemplateField


class Command(BaseCommand):
    """
    Заполняет базу тестовыми данными (seed)
    TURN - включает (True) заполнение данными БД
    """
    TURN = True
    COUNTER = 1000

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== Очищаем старые данные ==="))

        User = get_user_model()

        Template.objects.all().delete()
        TemplateField.objects.all().delete()
        Card.objects.all().delete()
        Log.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS("Данные очищены!"))

        if not self.TURN:
            sys.exit(0)

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
        template, _ = Template.objects.get_or_create(
            title="Резюме",
            description=fake.text(),
        )
        template_organization, _ = Template.objects.get_or_create(
            title="Организация",
            description=fake.text(),
        )

        # --- Поля шаблона ---
        field_name, _ = TemplateField.objects.get_or_create(
            template=template,
            title="ФИО",
            field_type=TemplateField.TypeField.TEXT,
            description=fake.text(),
            is_required=True,
            is_primary=True,
        )
        field_birth, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Дата рождения",
            field_type=TemplateField.TypeField.DATE,
            description=fake.text(),
        )
        field_experience, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Опыт (лет)",
            field_type=TemplateField.TypeField.NUMBER,
            description=fake.text(),
        )
        field_email, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Email",
            field_type=TemplateField.TypeField.EMAIL,
            description=fake.text(),
        )
        field_images, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Фотография",
            field_type=TemplateField.TypeField.IMAGE,
            description=fake.text(),
        )
        field_bio, _ = TemplateField.objects.get_or_create(
            template=template,
            title="Биография",
            field_type=TemplateField.TypeField.TEXT,
            description=fake.text(),
        )
        # Поля шаблона организации
        field_name_organization, _ = TemplateField.objects.get_or_create(
            template=template_organization,
            title="ИНН",
            field_type=TemplateField.TypeField.TEXT,
            is_required=True,
            is_primary=True,
            description=fake.text(),
        )

        # --- Генерация 100 записей ---
        for i in range(self.COUNTER):
            created_user = choice([user1, user2, user3, user4])

            # Создание карточки резюме
            resume_values = {
                "ФИО": fake.name(),
                "Дата рождения": fake.date_of_birth(minimum_age=18, maximum_age=60).isoformat(),
                "Опыт (лет)": randint(0, 30),
                "Email": fake.email(),
                "Фотография": fake.image_url(),
                "Биография": fake.texts(),
            }

            entity = Card.objects.create(
                template=template,
                created=created_user,
                values=resume_values,
            )

            # Лог действия
            Log.objects.create(
                user=created_user,
                action="Создание резюме",
                details=f"Создано резюме {entity.id}",
            )

            # Создание карточки организации
            inn = randrange(1000000000, 9999999999)
            organization_values = {
                "ИНН": str(inn),
            }

            entity_organization = Card.objects.create(
                template=template_organization,
                created=created_user,
                values=organization_values,
            )

            # Лог действия для организации
            Log.objects.create(
                user=created_user,
                action="Создание организации",
                details=f"Создана организация {entity_organization.id}",
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Создано {self.COUNTER} резюме и {self.COUNTER} организаций"))
