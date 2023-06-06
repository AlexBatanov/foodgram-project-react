from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe


User = get_user_model()


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites')


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart')
