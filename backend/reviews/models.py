from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from users.models import User

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
    quantity = models.PositiveIntegerField(verbose_name='Количество', null=True)
    measurement_unit = models.CharField(max_length=50, verbose_name='кг')
    
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
    image = models.ImageField(verbose_name='Изображение блюда', blank=True, null=True)
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


class IsFaworite(models.Model):
    user = models.ForeignKey(User, related_name='faworites', on_delete=models.CASCADE)
    recepe = models.ForeignKey(Recipe, related_name='faworites', on_delete=models.CASCADE)

class ShoppingCard(models.Model):
    user = models.ForeignKey(User, related_name='shoppingcard', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='shoppingcard', on_delete=models.CASCADE)





