from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        'Ник',
        unique=True,
        max_length=settings.USERNAME_MAX_LEN,
        validators=[validate_username]
    )
    email = models.EmailField(
        'E-mail',
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=settings.ROLE_MAX_LEN,
        choices=ROLE_CHOICES,
        help_text='Назначьте роль пользователя',
        default=USER,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.CONF_CODE_MAX_LEN,
        blank=True,
        default='null',
    )
    token = models.TextField(
        'Токен',
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id', ]
