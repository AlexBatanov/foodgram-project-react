from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователей."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail пользователя')
    password = models.CharField(max_length=100, blank=True)


class Tag(models.Model):
    name = models.CharField(max_length=250, verbose_name='Тег')
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Slug'
    )
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    units_of_measurement = models.PositiveIntegerField(
        verbose_name='Вес в граммах'
    )
    def __str__(self):
        return self.name

    
class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(verbose_name='Изображение блюда')
    description = models.TextField(verbose_name='Описание рецепта')

    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipe',
        through='RecipeIngredient',
        verbose_name='Ингредиент'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='Тег'
    )

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.recipe.name + ' ' + self.ingredient.name
    

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE
    )






