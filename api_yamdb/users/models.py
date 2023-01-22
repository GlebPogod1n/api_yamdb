from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models

USER_ROLE_USER = 'user'
USER_ROLE_MODERATOR = 'moderator'
USER_ROLE_ADMIN = 'admin'

USER_ROLE_CHOICES = (
    (USER_ROLE_USER, 'Пользователь'),
    (USER_ROLE_MODERATOR, 'Модератор'),
    (USER_ROLE_ADMIN, 'Админ'),
)


class User(AbstractUser):
    """Класс модели пользователя"""

    username = models.CharField(
        max_length=100,
        verbose_name='Псевдоним',
        db_index=True,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True
    )

    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
        validators=[EmailValidator(
            message='Введите корректный email'
        )]
    )

    role = models.CharField(
        max_length=30,
        verbose_name='Роль',
        choices=USER_ROLE_CHOICES,
        default=USER_ROLE_USER,
    )

    bio = models.TextField(
        verbose_name='биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        if self.role == USER_ROLE_USER:
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == USER_ROLE_MODERATOR:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == USER_ROLE_ADMIN:
            return True
        else:
            return False
