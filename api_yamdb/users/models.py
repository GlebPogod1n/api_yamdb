from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator
from django.db import models


class User(AbstractUser):
    """Класс модели пользователя"""

    username = models.CharField(
        max_length=100,
        verbose_name='Псевдоним',
        db_index=True,
        unique=True,
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
        max_length=200,
        verbose_name='email',
        unique=True,
        validators=[EmailValidator(
            message='Введите корректный email'
        )]
    )

    role = models.CharField(
        max_length=30,
        verbose_name='Роль',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Поле роли содержит недопустимый символ'
        )]
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
