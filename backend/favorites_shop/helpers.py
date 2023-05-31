import os

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from backend.settings import MEDIA_ROOT
from recipes.models import Recipe


def add_recipe_in_card_favorite(request, pk, serializer, model):
    """Добавление, удаление рецептов из избранных или карты покупок"""

    recipe = get_object_or_404(Recipe, pk=pk)
    obj = model.objects.filter(user=request.user, recipe=recipe)

    if request.method == 'POST':
        if obj:
            return Response(data='Уже добавлен', status=status.HTTP_400_BAD_REQUEST)
        
        model.objects.create(user=request.user, recipe=recipe)
        return Response(
            data=serializer(recipe).data,
            status=status.HTTP_200_OK
        )
    
    if obj:
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(data='Не добавлен', status=status.HTTP_400_BAD_REQUEST)


def create_shopping_dict(shopping_cart):
    """
    Проходимся по рецептам
    Добавляем в словарь ингредиенты
    Суммируем количество одинаковых ингредиентов
    """

    ingr_dict = dict()

    for obj_cart in shopping_cart:
        for ingr_amount in obj_cart.recipe.ingredients.all():
                ingr_name = (f'{ingr_amount.ingredient.name} '
                            f'({ingr_amount.ingredient.measurement_unit})')
                ingr_dict[ingr_name] = ingr_dict.get(ingr_name, 0) + \
                                       ingr_amount.amount
    return ingr_dict


def create_shopping_cart_txt(ingr_dict):
    """Создаем файл с ингредиентами и их колличеством"""

    filename = 'shopping_cart.txt'
    file_path = os.path.join(MEDIA_ROOT, filename)

    with open(file_path, 'w+') as f:
        for key, value in ingr_dict.items():
            f.write(f'{key} - {value}\n')
