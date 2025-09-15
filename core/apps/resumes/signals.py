from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.card import Card
from .models.template_field import TemplateField


@receiver(post_save, sender=Card)
def update_entity_main_name(sender, instance, **kwargs):
    primary_fields = TemplateField.objects.filter(
        template=instance.template,
        is_primary=True,
    )
    for primary_field in primary_fields:
        field_title = primary_field.title

        if field_title in instance.values:
            field_value = instance.values[field_title]

            if field_value:
                instance.main_name = str(field_value)
                Card.objects.filter(pk=instance.pk).update(main_name=instance.main_name)
                return

    if not instance.main_name:
        instance.main_name = f"{instance.template.title} #{instance.id}"
        Card.objects.filter(pk=instance.pk).update(main_name=instance.main_name)
