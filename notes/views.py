from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Note
from .forms import NoteForm


# ============= АУТЕНТИФИКАЦИЯ =============

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('note_list')
    else:
        form = UserCreationForm()
    return render(request, 'notes/register.html', {'form': form})


class CustomLoginView(LoginView):
    """Кастомная страница входа"""
    template_name = 'notes/login.html'

    def get_success_url(self):
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        return reverse_lazy('note_list')


def custom_logout(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('login')


# ============= ЗАМЕТКИ =============

class NoteListView(LoginRequiredMixin, ListView):
    """Список всех заметок пользователя"""
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает только заметки текущего пользователя"""
        return Note.objects.filter(author=self.request.user).order_by('-updated_at')


@login_required
def note_search(request):
    """Поиск заметок"""
    query = request.GET.get('q', '')
    notes = Note.objects.filter(author=request.user)

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'query': query,
        'is_search': True
    })


class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Детальный просмотр заметки"""
    model = Note
    template_name = 'notes/note_detail.html'

    def test_func(self):
        """Проверка, что пользователь - автор заметки"""
        note = self.get_object()
        return self.request.user == note.author


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Создание новой заметки"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('note_list')

    def form_valid(self, form):
        """Автоматически привязываем заметку к текущему пользователю"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Заметка успешно создана!')
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование заметки"""
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def test_func(self):
        """Проверка, что пользователь - автор заметки"""
        note = self.get_object()
        return self.request.user == note.author

    def form_valid(self, form):
        """Сообщение об успешном обновлении"""
        messages.success(self.request, 'Заметка успешно обновлена!')
        return super().form_valid(form)

    def get_success_url(self):
        """Перенаправление на страницу заметки после редактирования"""
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление заметки"""
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def test_func(self):
        """Проверка, что пользователь - автор заметки"""
        note = self.get_object()
        return self.request.user == note.author

    def delete(self, request, *args, **kwargs):
        """Сообщение об успешном удалении"""
        messages.success(self.request, 'Заметка успешно удалена!')
        return super().delete(request, *args, **kwargs)