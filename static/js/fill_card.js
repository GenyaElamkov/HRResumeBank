
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

    // Для корректной работы ID с подчеркиваниями
    // document.addEventListener('DOMContentLoaded', function() {
    //     // Автоматическая замена ID с подчеркиваниями на пробелы для корректной работы
    //     document.querySelectorAll('[id^="id_"]').forEach(el => {
    //         el.id = el.id.replace(/_/g, ' ')
    //     })
    // })
