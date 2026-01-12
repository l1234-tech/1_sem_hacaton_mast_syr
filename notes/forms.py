from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """Форма для создания и редактирования заметок"""

    class Meta:
        model = Note
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок заметки',
                'autofocus': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Начните писать свою заметку здесь...'
            }),
        }

        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }

        help_texts = {
            'title': 'Краткое название вашей заметки',
            'content': 'Основной текст заметки',
        }

    def clean_title(self):
        """Валидация заголовка"""
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise forms.ValidationError('Заголовок должен содержать минимум 3 символа')
        if len(title) > 200:
            raise forms.ValidationError('Заголовок не может превышать 200 символов')
        return title

    def clean_content(self):
        """Валидация содержания"""
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 10:
            raise forms.ValidationError('Заметка должна содержать минимум 10 символов')
        return content