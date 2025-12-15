
    // Добавляем стили Bootstrap к полям формы
    document.addEventListener('DOMContentLoaded', function() {
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (!input.classList.contains('form-control')) {
                input.classList.add('form-control');
            }
        });

        // Валидация формы
        const forms = document.querySelectorAll('.needs-validation');
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    });

    // Обработка удаления изображений
    document.querySelectorAll('.delete-image-btn').forEach(button => {
        button.addEventListener('click', function() {
            const imageId = this.getAttribute('data-image-id');
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });

    // Обработка удаления файлов
    document.querySelectorAll('.delete-file-btn').forEach(button => {
        button.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');
            const url = this.getAttribute('data-file-url');
            window.location.href = url;
        });
    });


// Добавляем обработчик для кнопки сохранения
document.addEventListener('DOMContentLoaded', function() {
    const buttonsWrapper = document.querySelector('.sticky-buttons-wrapper');
    const footer = document.querySelector('footer');
    const mainForm = document.getElementById('update-card-form');

    if (buttonsWrapper && footer && mainForm) {
        const saveButton = buttonsWrapper.querySelector('button[type="submit"]');
        if (saveButton && !saveButton.getAttribute('form')) {
            saveButton.setAttribute('form', mainForm.id);
        }

        function checkFooterDistance() {
            const footerRect = footer.getBoundingClientRect();
            const windowHeight = window.innerHeight;

            // Если футер близко к видимой области
            if (footerRect.top < windowHeight + 200) {
                buttonsWrapper.classList.add('near-footer');
            } else {
                buttonsWrapper.classList.remove('near-footer');
            }
        }

        window.addEventListener('scroll', checkFooterDistance);
        window.addEventListener('resize', checkFooterDistance);

        // Проверяем начальное состояние
        setTimeout(checkFooterDistance, 100);
    }
});