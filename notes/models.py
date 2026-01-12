from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    """Модель заметки"""
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок"
    )
    content = models.TextField(
        verbose_name="Содержание"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Автор"
    )

    # Метаданные модели
    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ['-updated_at']  # Сортировка по дате обновления (новые сверху)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для доступа к деталям заметки"""
        return reverse('note_detail', kwargs={'pk': self.pk})

    def get_short_content(self, length=100):
        """Возвращает укороченное содержание"""
        if len(self.content) > length:
            return self.content[:length] + "..."
        return self.content