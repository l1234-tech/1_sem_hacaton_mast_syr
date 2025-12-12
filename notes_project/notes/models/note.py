from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Пользователь',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст заметки',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения',
    )
    # Теги храним строкой через запятую, например: "учёба, django, важное"
    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Теги',
        help_text='Перечислите теги через запятую',
    )

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title