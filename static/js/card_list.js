    document.body.addEventListener('htmx:beforeRequest', function(e) {
        e.detail.target.classList.add('loading');
    });

    document.body.addEventListener('htmx:afterRequest', function(e) {
        e.detail.target.classList.remove('loading');
    });

    // Функция для поиска резюме
    function searchResumes() {
        const searchTerm = document.getElementById('searchInput').value;
        htmx.ajax('GET', `/?search=${encodeURIComponent(searchTerm)}`, {
            target: '#card-list',
            swap: 'innerHTML'
        });
    }