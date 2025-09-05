from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.entity_date import EntityDate


@receiver(post_save, sender=EntityDate)
def update_entity_main_name(sender, instance, **kwargs):
    field = instance.field
    entity = instance.entity

    # если поле основное — обновляем main_name у Entity
    if field.is_primary:
        value = (
            instance.value_text
            or instance.value_number
            or instance.value_date
            or instance.value_boolean
            or (instance.file.original_name if instance.file else None)
        )
        entity.main_name = str(value) if value else None
        entity.save(update_fields=["main_name"])
