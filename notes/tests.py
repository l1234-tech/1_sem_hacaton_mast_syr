"""
Тесты для приложения notes.
Запуск тестов: python manage.py test notes
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note
from .forms import NoteForm


# ==================== МОДЕЛИ ====================

class NoteModelTest(TestCase):
    """Тестирование модели Note"""

    def setUp(self):
        """Создание тестовых данных"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.note = Note.objects.create(
            title='Тестовая заметка',
            content='Содержание тестовой заметки',
            author=self.user
        )

    def test_note_creation(self):
        """Тест создания заметки"""
        self.assertEqual(self.note.title, 'Тестовая заметка')
        self.assertEqual(self.note.content, 'Содержание тестовой заметки')
        self.assertEqual(self.note.author, self.user)
        self.assertIsNotNone(self.note.created_at)
        self.assertIsNotNone(self.note.updated_at)

    def test_note_str_method(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.note), 'Тестовая заметка')

    def test_note_get_absolute_url(self):
        """Тест получения URL заметки"""
        url = self.note.get_absolute_url()
        expected_url = reverse('note_detail', kwargs={'pk': self.note.pk})
        self.assertEqual(url, expected_url)

    def test_note_get_short_content(self):
        """Тест сокращенного содержания"""
        # Тест с коротким текстом
        short_note = Note.objects.create(
            title='Короткая',
            content='Короткий текст',
            author=self.user
        )
        self.assertEqual(short_note.get_short_content(), 'Короткий текст')

        # Тест с длинным текстом
        long_text = 'A' * 150  # 150 символов
        long_note = Note.objects.create(
            title='Длинная',
            content=long_text,
            author=self.user
        )
        self.assertEqual(len(long_note.get_short_content()), 103)  # 100 + "..."

    def test_note_ordering(self):
        """Тест сортировки заметок"""
        # Создаем вторую заметку
        note2 = Note.objects.create(
            title='Вторая заметка',
            content='Новая заметка',
            author=self.user
        )

        notes = Note.objects.all()
        # Последняя созданная заметка должна быть первой
        self.assertEqual(notes[0], note2)
        self.assertEqual(notes[1], self.note)


# ==================== ФОРМЫ ====================

class NoteFormTest(TestCase):
    """Тестирование форм"""

    def test_valid_form(self):
        """Тест валидной формы"""
        form_data = {
            'title': 'Тестовая заметка',
            'content': 'Содержание заметки для теста'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_empty_title(self):
        """Тест формы с пустым заголовком"""
        form_data = {
            'title': '',
            'content': 'Содержание заметки'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_short_title(self):
        """Тест формы с коротким заголовком"""
        form_data = {
            'title': 'AB',  # Меньше 3 символов
            'content': 'Содержание'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_long_title(self):
        """Тест формы с длинным заголовком"""
        form_data = {
            'title': 'A' * 201,  # Больше 200 символов
            'content': 'Содержание'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_short_content(self):
        """Тест формы с коротким содержанием"""
        form_data = {
            'title': 'Заголовок',
            'content': 'Коротко'  # Меньше 10 символов
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_widgets(self):
        """Тест виджетов формы"""
        form = NoteForm()
        self.assertIn('class="form-control"', str(form['title']))
        self.assertIn('class="form-control"', str(form['content']))
        self.assertIn('placeholder="Введите заголовок заметки"', str(form['title']))
        self.assertIn('rows="10"', str(form['content']))


# ==================== ПРЕДСТАВЛЕНИЯ ====================

class ViewTests(TestCase):
    """Тестирование представлений"""

    def setUp(self):
        """Настройка тестового клиента и пользователя"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        # Создаем заметки для тестов
        self.note = Note.objects.create(
            title='Тестовая заметка',
            content='Содержание',
            author=self.user
        )

        self.note2 = Note.objects.create(
            title='Заметка другого пользователя',
            content='Секретное содержание',
            author=self.other_user
        )

    # ---------- Аутентификация ----------

    def test_login_view_get(self):
        """Тест GET запроса к странице входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/login.html')
        self.assertContains(response, 'Вход в систему')

    def test_login_view_post_valid(self):
        """Тест успешного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('note_list'))

    def test_login_view_post_invalid(self):
        """Тест неуспешного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Неверное имя пользователя или пароль')

    def test_register_view_get(self):
        """Тест GET запроса к странице регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/register.html')
        self.assertContains(response, 'Регистрация')

    def test_register_view_post_valid(self):
        """Тест успешной регистрации"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })
        # После регистрации должен быть редирект на список заметок
        self.assertRedirects(response, reverse('note_list'))

        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_logout_view(self):
        """Тест выхода из системы"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))

    # ---------- Заметки (неавторизованный) ----------

    def test_note_list_requires_login(self):
        """Тест, что список заметок требует авторизации"""
        response = self.client.get(reverse('note_list'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("note_list")}')

    def test_note_create_requires_login(self):
        """Тест, что создание заметки требует авторизации"""
        response = self.client.get(reverse('note_create'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("note_create")}')

    # ---------- Заметки (авторизованный) ----------

    def test_note_list_authenticated(self):
        """Тест списка заметок для авторизованного пользователя"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, 'Тестовая заметка')
        # Не должен видеть заметки другого пользователя
        self.assertNotContains(response, 'Заметка другого пользователя')

    def test_note_detail_authenticated(self):
        """Тест детального просмотра своей заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_detail', args=[self.note.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, 'Тестовая заметка')
        self.assertContains(response, 'Содержание')

    def test_note_detail_other_user(self):
        """Тест попытки просмотра чужой заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_detail', args=[self.note2.pk]))

        # Должен получить 403 Forbidden или редирект
        self.assertEqual(response.status_code, 403)

    def test_note_create_get(self):
        """Тест GET запроса к созданию заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertContains(response, 'Создание заметки')

    def test_note_create_post(self):
        """Тест POST запроса на создание заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('note_create'), {
            'title': 'Новая заметка',
            'content': 'Содержание новой заметки'
        })

        # Должен быть редирект на список заметок
        self.assertRedirects(response, reverse('note_list'))

        # Проверяем, что заметка создана
        self.assertTrue(Note.objects.filter(title='Новая заметка').exists())
        note = Note.objects.get(title='Новая заметка')
        self.assertEqual(note.author, self.user)

    def test_note_update_get(self):
        """Тест GET запроса к обновлению заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_update', args=[self.note.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertContains(response, 'Редактирование заметки')

    def test_note_update_post(self):
        """Тест POST запроса на обновление заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('note_update', args=[self.note.pk]), {
            'title': 'Обновленный заголовок',
            'content': 'Обновленное содержание'
        })

        # Должен быть редирект на детальную страницу заметки
        self.assertRedirects(response, reverse('note_detail', args=[self.note.pk]))

        # Проверяем обновление
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Обновленный заголовок')

    def test_note_update_other_user(self):
        """Тест попытки обновить чужую заметку"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_update', args=[self.note2.pk]))

        self.assertEqual(response.status_code, 403)

    def test_note_delete_get(self):
        """Тест GET запроса к удалению заметки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_delete', args=[self.note.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
        self.assertContains(response, 'Удаление заметки')

    def test_note_delete_post(self):
        """Тест POST запроса на удаление заметки"""
        self.client.login(username='testuser', password='testpass123')

        # Создаем заметку для удаления
        note_to_delete = Note.objects.create(
            title='Удаляемая заметка',
            content='Содержание',
            author=self.user
        )

        response = self.client.post(reverse('note_delete', args=[note_to_delete.pk]))

        # Должен быть редирект на список заметок
        self.assertRedirects(response, reverse('note_list'))

        # Проверяем, что заметка удалена
        self.assertFalse(Note.objects.filter(pk=note_to_delete.pk).exists())

    def test_note_delete_other_user(self):
        """Тест попытки удалить чужую заметку"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('note_delete', args=[self.note2.pk]))

        self.assertEqual(response.status_code, 403)

    def test_note_search(self):
        """Тест поиска заметок"""
        self.client.login(username='testuser', password='testpass123')

        # Создаем заметку с уникальным словом
        Note.objects.create(
            title='Уникальная заметка',
            content='Содержание с словом Python',
            author=self.user
        )

        # Ищем по слову
        response = self.client.get(reverse('note_search'), {'q': 'Python'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Уникальная заметка')

        # Пустой поиск должен показывать все заметки
        response = self.client.get(reverse('note_search'), {'q': ''})
        self.assertContains(response, 'Тестовая заметка')
        self.assertContains(response, 'Уникальная заметка')


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

class IntegrationTests(TestCase):
    """Интеграционные тесты (сквозные сценарии)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_full_user_journey(self):
        """Полный сценарий пользователя: регистрация → вход → создание → редактирование → удаление"""

        # 1. Регистрация
        response = self.client.post(reverse('register'), {
            'username': 'journeyuser',
            'password1': 'journeypass123',
            'password2': 'journeypass123'
        })
        self.assertRedirects(response, reverse('note_list'))

        # 2. Вход
        self.client.login(username='journeyuser', password='journeypass123')

        # 3. Создание заметки
        response = self.client.post(reverse('note_create'), {
            'title': 'Заметка путешествия',
            'content': 'Первая заметка нового пользователя'
        })
        self.assertRedirects(response, reverse('note_list'))

        note = Note.objects.get(title='Заметка путешествия')

        # 4. Редактирование заметки
        response = self.client.post(reverse('note_update', args=[note.pk]), {
            'title': 'Обновленная заметка',
            'content': 'Обновленное содержание'
        })
        self.assertRedirects(response, reverse('note_detail', args=[note.pk]))

        note.refresh_from_db()
        self.assertEqual(note.title, 'Обновленная заметка')

        # 5. Удаление заметки
        response = self.client.post(reverse('note_delete', args=[note.pk]))
        self.assertRedirects(response, reverse('note_list'))
        self.assertFalse(Note.objects.filter(pk=note.pk).exists())

    def test_note_pagination(self):
        """Тест пагинации списка заметок"""
        self.client.login(username='testuser', password='testpass123')

        # Создаем 15 заметок
        for i in range(15):
            Note.objects.create(
                title=f'Заметка {i}',
                content=f'Содержание {i}',
                author=self.user
            )

        # Первая страница
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)

        # Проверяем контекст пагинации
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['notes']), 10)  # paginate_by = 10

        # Вторая страница
        response = self.client.get(reverse('note_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['notes']), 5)  # 15 - 10 = 5


# ==================== API ТЕСТЫ (если будет API) ====================

class APITests(TestCase):
    """Тесты для API (если будет добавлено)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        self.note = Note.objects.create(
            title='API заметка',
            content='Содержание для API',
            author=self.user
        )

    def test_note_list_api(self):
        """Тест API списка заметок (пример)"""
        # Если добавите API, здесь будут тесты
        pass


# ==================== ТЕСТЫ БЕЗОПАСНОСТИ ====================

class SecurityTests(TestCase):
    """Тесты безопасности"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='securityuser',
            password='securitypass123'
        )
        self.other_user = User.objects.create_user(
            username='hacker',
            password='hackerpass123'
        )
        self.note = Note.objects.create(
            title='Секретная заметка',
            content='Конфиденциальная информация',
            author=self.user
        )

    def test_xss_protection(self):
        """Тест защиты от XSS атак"""
        self.client.login(username='securityuser', password='securitypass123')

        xss_payload = '<script>alert("XSS")</script>'
        response = self.client.post(reverse('note_create'), {
            'title': 'XSS тест',
            'content': xss_payload
        })

        # После создания проверяем, что скрипт экранирован
        note = Note.objects.get(title='XSS тест')
        response = self.client.get(reverse('note_detail', args=[note.pk]))

        # В HTML не должно быть тега script
        self.assertNotContains(response, '<script>')
        self.assertContains(response, '&lt;script&gt;')  # Должно быть экранировано

    def test_sql_injection_protection(self):
        """Тест защиты от SQL инъекций"""
        # Django ORM защищает от SQL инъекций, но проверим
        self.client.login(username='securityuser', password='securitypass123')

        sql_payload = "'; DROP TABLE notes_note; --"
        response = self.client.post(reverse('note_create'), {
            'title': 'SQL тест',
            'content': sql_payload
        })

        # Если всё хорошо, заметка создастся
        self.assertTrue(Note.objects.filter(title='SQL тест').exists())

        # И таблица notes_note всё ещё существует
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notes_note';")
            tables = cursor.fetchall()
            self.assertTrue(any('notes_note' in table for table in tables))


# ==================== ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ ====================

class PerformanceTests(TestCase):
    """Тесты производительности (базовые)"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='perfuser',
            password='perfpass123'
        )
        self.client.login(username='perfuser', password='perfpass123')

    def test_note_list_performance(self):
        """Тест производительности списка заметок"""
        import time

        # Создаем 100 заметок
        for i in range(100):
            Note.objects.create(
                title=f'Заметка {i}',
                content=f'Содержание {i}',
                author=self.user
            )

        start_time = time.time()
        response = self.client.get(reverse('note_list'))
        end_time = time.time()

        self.assertEqual(response.status_code, 200)

        # Время выполнения должно быть меньше 1 секунды
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)
        print(f"Время выполнения списка 100 заметок: {execution_time:.3f} сек")


# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == '__main__':
    # Для запуска тестов напрямую из файла
    import django

    django.setup()
    from django.test.utils import setup_test_environment
    from django.test.runner import DiscoverRunner

    setup_test_environment()
    runner = DiscoverRunner()
    runner.run_tests(['notes'])