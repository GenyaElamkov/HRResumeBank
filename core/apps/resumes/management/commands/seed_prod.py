from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.apps.resumes.fixtures.initial_data import CARD_VALUES
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template
from core.apps.resumes.models.template_field import TemplateField


TEMPLATE_FIELDS = {
    "photo": "Фотография",
    "full_name": "ФИО",
    "birth_date": "Дата рождения",
    "position": "Должность",
    "department": "Подразделение",
    "directorate": "Дирекция",
    "block": "Блок",
    "manager": "Куратор",
    "branch": "Филиал",
    "hire_date": "Дата приема",
    "employment": "Трудоустройство",
    "base_office": "Базовый офис (location)",
    "status": "Статус",
    "termination_transfer_date": "Дата увольнения/перевода",
    "reason": "Причина",
    "old_full_name": "Старое ФИО",
    "birth_place": "Место рождения",
    "citizenship": "Гражданство",
    "passport": "Паспорт",
    "inn": "ИНН",
    "registration_address": "Адрес регистрации",
    "residential_address": "Адрес проживания",
    "additional_addresses": "Дополнительно установленные адреса",
    "phone": "Телефон",
    "additional_phones": "Дополнительно установленные телефоны",
    "telegram": "Телеграмм",
    "telegram_interests": "Интересы в телерамм",
    "additional_telegrams": "Дополнительные ТГ",
    "personal_email": "Email (личный)",
    "work_email": "Email (рабочий)",
    "social_networks": "Социальные сети",
    "education": "Образование",
    "workplace": "Место работы",
    "legal_entities_participation": "Участие вдеятельности юридических лиц",
    "relatives": "Родственники",
    "referrer": "Рекомендатель",
    "company_affiliation": "Аффилированность в компании (родств., друзья и т.д.)",
    "attention_required_info": "Информация, требующая внимания",
    "work_mode": "Режим работы (Удаленно/Офис/Гибрид)",
    "archive": "Архив",
}


class Command(BaseCommand):
    """
    Заполняет базу тестовыми данными (seed)
    """

    def handle(self, *args, **options):
        User = get_user_model()

        # Пользователи
        user, _ = User.objects.get_or_create(
            username="user",
        )

        # Шаблоны
        template, _ = Template.objects.get_or_create(
            title="Карточка сотрудника (кандидата)",
            description="Шаблон для хранения персональных и рабочих данных сотрудников и кандидатов",
        )

        # Поля шаблона
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['photo'],
            field_type=TemplateField.TypeField.IMAGE,
            is_visible=True,
            order=0,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['full_name'],
            field_type=TemplateField.TypeField.TEXT,
            is_required=True,
            is_primary=True,
            is_visible=True,
            order=1,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['birth_date'],
            field_type=TemplateField.TypeField.DATE,
            order=2,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['position'],
            field_type=TemplateField.TypeField.TEXT,
            is_visible=True,
            order=3,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['department'],
            field_type=TemplateField.TypeField.TEXT,
            order=4,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['directorate'],
            field_type=TemplateField.TypeField.TEXT,
            order=5,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['block'],
            field_type=TemplateField.TypeField.TEXT,
            order=6,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['manager'],
            field_type=TemplateField.TypeField.TEXT,
            order=7,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['branch'],
            field_type=TemplateField.TypeField.TEXT,
            order=9,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['hire_date'],
            field_type=TemplateField.TypeField.DATE,
            order=10,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['employment'],
            field_type=TemplateField.TypeField.TEXT,
            order=11,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['base_office'],
            field_type=TemplateField.TypeField.TEXT,
            order=12,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['status'],
            field_type=TemplateField.TypeField.TEXT,
            order=13,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['termination_transfer_date'],
            field_type=TemplateField.TypeField.DATE,
            order=14,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['reason'],
            field_type=TemplateField.TypeField.TEXT,
            order=15,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['old_full_name'],
            field_type=TemplateField.TypeField.TEXT,
            order=16,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['birth_place'],
            field_type=TemplateField.TypeField.TEXT,
            order=17,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['citizenship'],
            field_type=TemplateField.TypeField.TEXT,
            order=18,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['passport'],
            field_type=TemplateField.TypeField.TEXT,
            order=19,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['inn'],
            field_type=TemplateField.TypeField.TEXT,
            order=20,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['registration_address'],
            field_type=TemplateField.TypeField.TEXT,
            order=21,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['residential_address'],
            field_type=TemplateField.TypeField.TEXT,
            order=22,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['additional_addresses'],
            field_type=TemplateField.TypeField.TEXT,
            order=23,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['phone'],
            field_type=TemplateField.TypeField.TEXT,
            order=24,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['additional_phones'],
            field_type=TemplateField.TypeField.TEXT,
            order=25,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['telegram'],
            field_type=TemplateField.TypeField.TEXT,
            order=26,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['telegram_interests'],
            field_type=TemplateField.TypeField.TEXT,
            order=27,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['additional_telegrams'],
            field_type=TemplateField.TypeField.TEXT,
            order=28,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['personal_email'],
            field_type=TemplateField.TypeField.EMAIL,
            order=29,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['work_email'],
            field_type=TemplateField.TypeField.EMAIL,
            order=30,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['social_networks'],
            field_type=TemplateField.TypeField.TEXT,
            order=31,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['education'],
            field_type=TemplateField.TypeField.TEXT,
            order=32,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['workplace'],
            field_type=TemplateField.TypeField.TEXT,
            order=33,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['legal_entities_participation'],
            field_type=TemplateField.TypeField.TEXT,
            order=34,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['relatives'],
            field_type=TemplateField.TypeField.TEXT,
            order=35,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['referrer'],
            field_type=TemplateField.TypeField.TEXT,
            order=36,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['company_affiliation'],
            field_type=TemplateField.TypeField.TEXT,
            order=37,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['attention_required_info'],
            field_type=TemplateField.TypeField.TEXT,
            order=38,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['work_mode'],
            field_type=TemplateField.TypeField.CHOICE,
            choices="Удаленно,Офис,Гибрид",
            order=39,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['archive'],
            field_type=TemplateField.TypeField.FILE,
            order=40,
        )

        counter = 0

        # Создание карточки резюме
        for counter, card_data in enumerate(CARD_VALUES, 0):
            created_user = user
            resume_values = {}
            for value in TEMPLATE_FIELDS.values():
                if value in ["Фотография", "Архив"]:
                    continue

                resume_values[value] = card_data[value]

            Card.objects.create(
                template=template,
                created=created_user,
                values=resume_values,
            )
            counter += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Создано {counter} карточек резюме"))
