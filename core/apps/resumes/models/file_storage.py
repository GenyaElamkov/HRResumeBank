import os
import uuid

from django.db import models

from core.apps.common.models import TimeBaseModel


def _get_uploaded_file_name(instance, filename: str) -> str:
    """Генерация пути к файлу"""
    ext = os.path.splitext(filename)[1]
    allowed_extensions = [
        '.pdf', '.docx', '.doc', '.txt', '.jpg', '.jpeg', '.png', '.xlsx', '.xls',
    ]

    if not ext.lower() in allowed_extensions:
        raise ValueError(f"Недопустимое расширение файла: {ext}")

    unique_filename = f"{os.path.splitext(os.path.basename(filename))[0]}_{uuid.uuid4()}"

    return f"storage/{instance.card.id}/{unique_filename}{ext}"


class FileStorage(TimeBaseModel):
    """Хранилище файлов"""
    card = models.ForeignKey(
        to="resumes.Card",
        verbose_name="Карточка",
        on_delete=models.CASCADE,
        related_name="storage",
    )

    uploaded_file = models.FileField(
        verbose_name="Путь к файлу",
        upload_to=_get_uploaded_file_name,
    )

    def __str__(self):
        return f"{self.card} / {os.path.basename(self.uploaded_file.name)}"

    class Meta:
        db_table = "file_storage"
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ['create_at']
        indexes = [
            models.Index(fields=['card', 'create_at']),
        ]
