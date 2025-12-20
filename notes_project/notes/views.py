from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Note
from .forms import NoteForm

@login_required
def note_list(request):
    """Список заметок текущего пользователя."""
    notes = Note.objects.filter(author=request.user).order_by('-updated_at')
    return render(request, 'notes/note_list.html', {'notes': notes})


@login_required
def note_detail(request, pk):
    """Детальный просмотр одной заметки."""
    note = get_object_or_404(Note, pk=pk, author=request.user)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_create(request):
    """Создание новой заметки."""
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user  # привязываем заметку к текущему пользователю
            note.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm()

    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def note_update(request, pk):
    """Редактирование существующей заметки."""
    note = get_object_or_404(Note, pk=pk, author=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes:note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_form.html', {'form': form, 'note': note})


@login_required
def note_delete(request, pk):
    """Удаление заметки."""
    note = get_object_or_404(Note, pk=pk, author=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('notes:note_list')

    # Показываем страницу с подтверждением удаления
    return render(request, 'notes/note_confirm_delete.html', {'note': note})