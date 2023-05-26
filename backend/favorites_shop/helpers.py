from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe


def add_recipe_in_card_favorite(request, pk, serializer, model):
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