from core.apps.resumes.forms import MultipleFileInput


class TestMultipleFileInput:
    """Проверка виджета MultipleFileInput для множественной загрузки файлов"""

    def test_allow_multiple_files(self):
        """Проверка, что виджет разрешает множественный выбор файлов"""
        widget = MultipleFileInput()
        assert widget.allow_multiple_selected is True

    def test_widget_render(self):
        """Проверка рендера виджета: атрибут multiple должен быть True"""
        widget = MultipleFileInput()
        rendered = widget.render('files', None)
        assert 'multiple' in rendered
