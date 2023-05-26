from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from recipes.models import Recipe
from favorites_shop.serializers import RecepeFavoritShopSerializer
from .models import Favorites

User = get_user_model()

class FavoritesView(viewsets.ViewSet):

    permission_classes = [IsAuthenticated,]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='favorite')
    def favorites_add(self, request, pk):

        recipe = get_object_or_404(Recipe, pk=pk)
        favorites = Favorites.objects.filter(user=request.user, recipe=recipe)

        if request.method == 'POST':
            if favorites:
                return Response(data='Уже добавлен', status=status.HTTP_400_BAD_REQUEST)
            
            Favorites.objects.create(user=request.user, recipe=recipe)
            return Response(
                data=RecepeFavoritShopSerializer(recipe).data,
                status=status.HTTP_200_OK
            )
        
        if favorites:
            favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(data='Не добавлен', status=status.HTTP_400_BAD_REQUEST)
