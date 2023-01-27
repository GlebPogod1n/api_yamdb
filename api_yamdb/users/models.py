from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс модели пользователя"""
    USER_ROLE_USER = 'user'
    USER_ROLE_MODERATOR = 'moderator'
    USER_ROLE_ADMIN = 'admin'
    USER_ROLE_CHOICES = (
        (USER_ROLE_USER, 'Пользователь'),
        (USER_ROLE_MODERATOR, 'Модератор'),
        (USER_ROLE_ADMIN, 'Админ'),
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
        verbose_name='email',
        unique=True,
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
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user'
            )
        ]

    @property
    def is_user(self):
        return self.role == self.USER_ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == self.USER_ROLE_ADMIN or self.is_superuser
