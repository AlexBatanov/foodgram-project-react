from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from ingredients.models import Ingredient
from .models import RecipeIngredient


def check_is_favorite_and_is_shoping_list(context, obj, model):
    """Проверяет нахождение объекта в избранном или в карте покупок"""

    user = context['request'].user
    return (
        user.is_authenticated and
        model.objects.filter(recipe=obj, user=user).exists()
    )


def create_ingredients_return_tags(data):
    """
    Проверяет наличие ингредиента по id
    создает объекты ингредиентов с количеством
    возвращает лист с объектами и теги
    """

    ingredients = data.pop('ingredients')
    tags = data.pop('tags')
    ingredients_list = []

    for ingredient in ingredients:
        ingredient_id, amount = ingredient.get('id'), ingredient.get('amount')
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        ingredien_amount = RecipeIngredient(ingredient=ingredient,
                                            amount=amount)
        ingredients_list.append(ingredien_amount)
    RecipeIngredient.objects.bulk_create(ingredients_list)

    return ingredients_list, tags


def checking_ownership(self, recipe):
    """Проверка на автора поста"""

    author = recipe.author
    user = self.request.user
    if author != user:
        raise PermissionDenied('Доступ запрещен')
