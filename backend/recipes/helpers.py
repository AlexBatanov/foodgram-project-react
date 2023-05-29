from django.shortcuts import get_object_or_404

from ingredients.models import Ingredient
from .models import RecipeIngredient


def chek_is_favorite_and_is_shoping_list(context, obj, model):
    """Проверяет нахождение объекта в избранном или в карте покупок"""

    user = context['request'].user
    return (
        user.is_authenticated and 
        model.objects.filter(recipe=obj, user=user).exists()
    )

def creat_ingredients(ingredients):
    """
    Проверяет наличие ингредиента по id
    создает объекты ингредиентов с количеством
    возвращает лист с объектами 
    """

    ingredients_list = []

    for ingredient in ingredients:
        ingredient_id, amount = ingredient.get('id'), ingredient.get('amount')
        ingredient = get_object_or_404(Ingredient, id=ingredient_id)
        ingredien_amount, _ = RecipeIngredient.objects.get_or_create(ingredient=ingredient, amount=amount)
        ingredients_list.append(ingredien_amount)

    return ingredients_list