import os
import uuid

from django.db import models

from core.apps.common.models import TimeBaseModel


def _get_uploaded_file_name(instance, filename: str) -> str:
    """Генерация пути к файлу"""
    ext = os.path.splitext(filename)[1]
    allowed_extensions = ['.jpg', '.jpeg', '.png']

    if not ext.lower() in allowed_extensions:
        raise ValueError(f"Недопустимое расширение файла: {ext}")

    unique_filename = f"{os.path.splitext(os.path.basename(filename))[0]}_{uuid.uuid4()}"

    return f"profile_image/{instance.card.id}/{unique_filename}{ext}"


class ProfileImage(TimeBaseModel):
    """Изображение профиля"""
    card = models.ForeignKey(
        to="resumes.Card",
        verbose_name="Карточка",
        on_delete=models.CASCADE,
        related_name="profile_image",
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to=_get_uploaded_file_name,
    )

    def __str__(self):
        return f"{self.card} / {os.path.basename(self.image.name) if self.image else 'no image'}"

    class Meta:
        db_table = "profile_image"
        verbose_name = "Изображение профиля"
        verbose_name_plural = "Изображения профиля"
        ordering = ['create_at']
        indexes = [
            models.Index(fields=['card', 'create_at']),
        ]
