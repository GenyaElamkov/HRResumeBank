import pytest

from core.apps.resumes.templatetags.strip_html import strip_html


@pytest.mark.parametrize(
    "html_input, cleaned_text", [
        # Пограничные случаи: пустая строка, None, пробелы
        ('', ''),
        (None, ''),
        ('   ', ''),
        ('\n\t\r', ''),

        # Простой HTML
        ('<p>Привет, <b>мир</b>!</p>', 'Привет, мир!'),

        # HTML с атрибутами
        ('<a href="http://example.com">Ссылка</a>', 'Ссылка'),

        # Стили и script-теги
        ('<div style="color:red">Текст <script>alert("xss")</script></div>', 'Текст alert("xss")'),

        # HTML-сущности
        ('&lt;div&gt; &amp; &quot;привет&quot;', '<div> & "привет"'),

        # Комбинация: HTML + сущности + лишние пробелы
        ('  <p>   Привет,   &nbsp;   <span>мир</span>!   </p>  ', 'Привет, мир!'),

        # Многострочный текст
        ('<ul>\n<li>Раз</li>\n<li>Два</li>\n</ul>', 'Раз Два'),

        # Одиночные теги. Полностью удаляются теги не заменяя их на пробелы
        ('Текст<br>с переносом<img src="x">.', 'Текстс переносом.'),
    ],
)
def test_strip_html_various_cases(html_input, cleaned_text):
    assert strip_html(html_input) == cleaned_text


def test_strip_html_with_non_string_input():
    # Проверка, что не-строковые значения корректно обрабатываются через str()
    assert strip_html(123) == '123'
    assert strip_html(True) == 'True'
    assert strip_html(0.5) == '0.5'


def test_strip_html_preserves_single_spaces():
    input_text = 'a  b   c    d'
    expected = 'a b c d'
    assert strip_html(input_text) == expected


def test_strip_html_removes_unicode_whitespace():
    # Тест на нормализацию различных видов пробелов (включая неразрывный пробел)
    input_text = 'Привет\u00A0&nbsp;\u2003миру!'
    expected = 'Привет миру!'
    assert strip_html(input_text) == expected
