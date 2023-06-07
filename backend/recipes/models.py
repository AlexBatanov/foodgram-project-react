from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from tags.models import Tag
from ingredients.models import Ingredient
from .constants import (MIN_AMOUNT, MAX_AMOUNT,
                        MIN_COOKING_TIME, MAX_COOKING_TIME)


User = get_user_model()


class RecipeIngredient(models.Model):
    """
    Ингредиент и его количество
    """

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        default=MIN_AMOUNT,
        validators=[MinValueValidator(MIN_AMOUNT),
                    MaxValueValidator(MAX_AMOUNT)],
        verbose_name='Количество'
    )

    class Meta:
        ordering = ['ingredient']

    def __str__(self):
        return f'{self.ingredient}'


class Recipe(models.Model):
    """
    Рецепт
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(verbose_name='Изображение блюда', blank=True)
    text = models.TextField(verbose_name='Описание рецепта')

    ingredients = models.ManyToManyField(
        RecipeIngredient,
        related_name='recipes',
        verbose_name='Ингредиент'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )

    cooking_time = models.PositiveSmallIntegerField(
        default=MIN_COOKING_TIME,
        validators=[MinValueValidator(MIN_COOKING_TIME),
                    MaxValueValidator(MAX_COOKING_TIME)],
        verbose_name='время готовки в минутах'
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
