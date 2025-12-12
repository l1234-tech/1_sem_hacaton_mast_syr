
from .category import Category
from .tag import Tag


class Note(models.Model):
    """
    Модель заметки.

    Поля:
    - пользователь (author/user)
    - заголовок
    - текст
    - дата создания
    - дата последнего изменения
    - категория (опционально)
    - теги (Many-to-Many)
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Пользователь',
        help_text='Пользователь, которому принадлежит эта заметка.',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Краткий заголовок заметки.',
    )
    text = models.TextField(
        verbose_name='Текст заметки',
        help_text='Основное содержимое заметки.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes',
        verbose_name='Категория',
        help_text='Категория, к которой относится заметка (необязательно).',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='notes',
        verbose_name='Теги',
        help_text='Список тегов, связанных с этой заметкой.',
    )

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-updated_at', '-created_at']

    def __str__(self) -> str:
        """
        Строковое представление заметки.
        Удобно видеть пользователя и заголовок.
        """
        return f'{self.user.username}: {self.title}'

    def get_tegs_list(self) -> list[str]:
        """
        Вспомогательная функция:
        возвращает список названий тегов у заметки.

        Удобно использовать в шаблонах или API,
        если нужно быстро получить названия тегов.
        """
        return [teg.name for teg in self.tags.all()]

    def get_tags_string(self, separator: str = ', ') -> str:
        """
        Вспомогательная функция:
        возвращает все теги одной строкой с указанным разделителем.

        По умолчанию разделитель — запятая с пробелом.
        """
        return separator.join(self.get_tegs_list())
