// Базовый JavaScript для сайта заметок

document.addEventListener('DOMContentLoaded', function() {
    console.log('Сайт заметок загружен');

    // Автоматическое скрытие сообщений через 5 секунд
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Подтверждение удаления
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить эту заметку?')) {
                e.preventDefault();
            }
        });
    });

    // Подсветка активной ссылки в навигации
    const currentUrl = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentUrl) {
            link.classList.add('active');
        }
    });

    // Подсветка поля поиска при фокусе
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        searchInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    }

    // Подсчет символов в текстовом поле
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        const counter = document.createElement('div');
        counter.className = 'text-muted small mt-1';
        counter.innerHTML = 'Символов: <span class="char-count">0</span>';
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            const count = this.value.length;
            counter.querySelector('.char-count').textContent = count;

            if (count > 1000) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });

        // Инициализируем счетчик
        textarea.dispatchEvent(new Event('input'));
    });
});

// Функция для копирования текста
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Текст скопирован в буфер обмена');
    }, function(err) {
        console.error('Ошибка копирования: ', err);
    });
}

// Функция для форматирования даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}