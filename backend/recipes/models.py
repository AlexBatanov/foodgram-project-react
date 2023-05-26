from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator 

from tags.models import Tag
from ingredients.models import Ingredient


User = get_user_model()

class Recipe(models.Model):
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
    image = models.ImageField(verbose_name='Изображение блюда')
    text = models.TextField(verbose_name='Описание рецепта')

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

    cooking_time = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='время готовки в минутах'
    )

    def __str__(self):
        return self.name
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )