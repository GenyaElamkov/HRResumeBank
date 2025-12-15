from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.apps.resumes.fixtures.initial_data import CARD_VALUES
from core.apps.resumes.models.card import Card
from core.apps.resumes.models.template import Template
from core.apps.resumes.models.template_field import TemplateField


TEMPLATE_FIELDS = {
    "verification": "Проверка",
    "name_CA": "Наименование КА",
    "TIN": "ИНН",
    "our_legal_entity": "Наше ЮЛ",
    "subtype_document": "Подвид документа",
    "document_name": "Наименование документа",
    "subject_contract": "Предмет договора и сумма",
    "review_date_SB": "Дата рассмотрения СБ",
    "initiator": "Инициатор",
    "comments": "Комментарии",
    "conclusion": "Заключение",
    "executor": "Исполнитель",
    "source": "Источник",
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
            username="savelii",
        )

        # Шаблоны
        template, _ = Template.objects.get_or_create(
            title="Карточка контрагента",
            description="Шаблон для хранения данных организаций",
        )

        # Поля шаблона
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['TIN'],
            field_type=TemplateField.TypeField.TEXT,
            is_required=True,
            is_primary=True,
            order=0,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['name_CA'],
            field_type=TemplateField.TypeField.TEXT,
            is_required=True,
            is_visible=True,
            order=1,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['verification'],
            field_type=TemplateField.TypeField.CHOICE,
            choices="ДД,Б,ПБ",
            order=2,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['our_legal_entity'],
            field_type=TemplateField.TypeField.TEXT,
            order=3,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['subtype_document'],
            field_type=TemplateField.TypeField.TEXT,
            order=4,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['document_name'],
            field_type=TemplateField.TypeField.TEXT,
            is_visible=True,
            order=5,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['subject_contract'],
            field_type=TemplateField.TypeField.TEXT,
            order=6,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['review_date_SB'],
            field_type=TemplateField.TypeField.DATE,
            order=7,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['initiator'],
            field_type=TemplateField.TypeField.TEXT,
            order=8,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['comments'],
            field_type=TemplateField.TypeField.TEXT,
            order=9,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['conclusion'],
            field_type=TemplateField.TypeField.CHOICE,
            choices="Согласовано,Не согласовано,На доработку,Согласовано с замечаниями",
            is_visible=True,
            order=10,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['executor'],
            field_type=TemplateField.TypeField.CHOICE,
            choices="Исецкий С.Е.,Шипицын Д.А.",
            order=11,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['source'],
            field_type=TemplateField.TypeField.TEXT,
            order=12,
        )
        TemplateField.objects.get_or_create(
            template=template,
            title=TEMPLATE_FIELDS['archive'],
            field_type=TemplateField.TypeField.FILE,
            order=13,
        )

        counter = 0

        # Создание карточки резюме
        for counter, card_data in enumerate(CARD_VALUES, 0):
            created_user = user
            resume_values = {}
            for value in TEMPLATE_FIELDS.values():
                if value in ["Фотография", "Архив"]:
                    continue
                if value in "ИНН":
                    resume_values[value] = f"ИНН: {card_data[value]}"
                else:
                    resume_values[value] = card_data[value]

            Card.objects.create(
                template=template,
                created=created_user,
                values=resume_values,
            )
            counter += 1
            if counter == 5:
                break

        self.stdout.write(self.style.SUCCESS(f"✅ Создано {counter} карточек резюме"))
