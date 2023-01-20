from django.contrib.auth import get_user_model
from django.db import models

from .validators import year_validator

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        db_index=True, max_length=256
    )
    year = models.IntegerField(
        verbose_name='Дата выпуска',
        validators=(year_validator,)
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=200,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='titles',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name
