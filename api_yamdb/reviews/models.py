import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models

from api_yamdb.settings import RATING_MAX, RATING_MIN

User = get_user_model()


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Genre(BaseModel):
    """Модель жанра."""
    name = models.CharField('Название жанра',
                            max_length=256,
                            unique=True,
                            validators=[RegexValidator])
    slug = models.SlugField('Краткое имя жанра',
                            max_length=50,
                            unique=True,
                            validators=[RegexValidator])

    def __str__(self):
        return self.name[:30]

    class Meta:
        ordering = ('name',)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(BaseModel):
    """Модель Категории."""
    name = models.CharField('Название категории',
                            max_length=256,
                            unique=True,
                            validators=[RegexValidator])
    slug = models.SlugField('Краткое имя категории',
                            max_length=50,
                            unique=True,
                            validators=[RegexValidator])

    def __str__(self):
        return self.name[:30]

    class Meta:
        ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Title(BaseModel):
    """Модель произведения."""
    name = models.CharField('Название произведения',
                            max_length=256,
                            validators=[RegexValidator])
    year = models.PositiveSmallIntegerField(
        'Год',
        validators=[MaxValueValidator(dt.datetime.now().year),
                    MinValueValidator(0)],
        blank=False,
        null=False)
    description = models.TextField('Описание', max_length=1000, blank=True,
                                   null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name[:30]

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class CreatedModel(BaseModel):
    """Абстрактная модель. Добавляет в модель дату создания.
    Упорядочивает записи по дате создания от новой к старой."""
    text = models.TextField(
        max_length=200,
        verbose_name='Текст сообщения',
        blank=False
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True


class Review(CreatedModel):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=[
            MaxValueValidator(RATING_MAX),
            MinValueValidator(RATING_MIN),
        ],
        blank=False,
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(CreatedModel):
    """Модель комментария."""
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарии'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date', ]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
