from django.db import models

class Tag(models.Model):
    """
    Тег (метка) для заметок.

    В отличие от категории (крупная тема),
    тег — более гибкая и свободная метка: 'важное', 'django', 'экзамен' и т.п.
    Одна заметка может иметь много тегов, и один тег может относиться
    к многим заметкам (связь Many-to-Many).
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название тега',
        help_text='Краткое имя тега, например: "важное" или "django".',
    )
    color = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Цвет (опционально)',
        help_text='Можно хранить название цвета или HEX-код, например "#ff0000".',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        """
        Возвращает человеко читаемое название тега.
        """
        return self.name