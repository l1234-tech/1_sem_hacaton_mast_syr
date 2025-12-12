from django.db import models


class Category(models.Model):
    """
    Категория заметок.

    Примеры: 'Учёба', 'Работа', 'Личное'.
    Используется для группировки заметок по крупным темам.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории',
        help_text='Краткое название категории, например: "Учёба" или "Работа".',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Дополнительное описание категории (необязательно).',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  # сортировка по названию

    def __str__(self) -> str:
        """
        Возвращает удобное строковое представление категории,
        которое будет использоваться в админке и при выводе объекта.
        """
        return self.name