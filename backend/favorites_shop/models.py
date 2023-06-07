from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe


User = get_user_model()


class Favorites(models.Model):
    """
    Избранные рецепты
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name} {self.recipe.name}'


class ShoppingCart(models.Model):
    """
    Карта покупок
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.name} {self.recipe.name}'
