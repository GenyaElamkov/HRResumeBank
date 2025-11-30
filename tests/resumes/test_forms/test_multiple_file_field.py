from django.forms import ValidationError

import pytest


class TestMultipleFileField:
    """Проверка виджета MultipleFileField для множественной загрузки файлов"""

    def test_validation_empty_valuy(self, fields):
        """Проверка, что поле не может быть пустым"""
        assert fields.validate(None) is None
        assert fields.validate([]) is None

    def test_validation_single_valid_file(self, fields, mock_file):
        """Проверка, что поле допускает валидный файл"""
        valid_file = mock_file("test_file.pdf")
        assert fields.validate(valid_file) is None

    @pytest.mark.parametrize(
        "file_name", [
            ("test_file.PDF"),
            ("test_file.pdf"),
            ("test_file.docx"),
            ("test_file.doc"),
            ("test_file.txt"),
            ("test_file.jpg"),
            ("test_file.jpeg"),
            ("test_file.png"),
            ("test_file.xlsx"),
            ("test_file.xls"),
        ],
    )
    def test_validation_multiple_valid_files(self, file_name, mock_file, fields):
        """Проверка, что поле допускает валидные файлы"""
        value = [mock_file(file_name)]
        try:
            fields.validate(value)
        except ValidationError as e:
            pytest.fail(f"Ошибка валидации: {e}")

    def test_validate_case_sensitive_extentions(self, mock_file, fields):
        """Проверка, что расширения файлов не чувствительны к регистру"""
        value = [mock_file("test_file.PDF")]
        try:
            fields.validate(value)
        except ValidationError as e:
            pytest.fail(f"Ошибка валидации: {e}")

    def test_validation_single_invalid_file(self, mock_file, fields):
        """Проверка, что поле не допускает невалидный файл"""
        invalid_file = mock_file("test_file.exe")
        with pytest.raises(ValidationError) as exc_info:
            fields.validate(invalid_file)
        assert "имеет недопустимое расширение '.exe'" in str(exc_info.value)

    def test_validate_mixed_extensions(self, mock_file, fields):
        """Проверка, что поле допускает файлы с разными расширениями"""
        valid_file = mock_file("test_file.pdf")
        invalid_file = mock_file("test_file.exe")
        with pytest.raises(ValidationError) as exc_info:
            fields.validate([valid_file, invalid_file])

        error_msg = str(exc_info.value)
        assert str(invalid_file) in error_msg
        assert ".exe" in error_msg
        assert "Разрешены" in error_msg
