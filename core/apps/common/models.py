from django.db import models


class TimeBaseModel(models.Model):
    create_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    update_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )

    class Meta:
        abstract = True
