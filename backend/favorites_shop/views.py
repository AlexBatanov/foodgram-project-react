import os

from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from backend.settings import MEDIA_ROOT
from .serializers import RecepeFavoritShopSerializer
from .models import Favorites, ShoppingCart
from .helpers import (add_recipe_in_card_favorite,
                      create_shopping_dict, create_shopping_cart_txt)

User = get_user_model()


class FavoritesView(viewsets.ViewSet):
    """
    Набор представлений для подписки и отписки на автора 
    """

    permission_classes = [IsAuthenticated,]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='favorite')
    def favorites_add(self, request, pk):
        return add_recipe_in_card_favorite(
            request=request,
            pk=pk, serializer=RecepeFavoritShopSerializer,
            model=Favorites
            )


class ShoppingCardView(viewsets.ViewSet):
    """
    Набор представлений для добавления, удаления рецепта в покупки
    и скачивания листа покупок в виде txt файла
    """
    permission_classes = [IsAuthenticated,]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='shopping_cart')
    def shopping_card_add(self, request, pk):
        return add_recipe_in_card_favorite(
            request=request, pk=pk,
            serializer=RecepeFavoritShopSerializer,
            model=ShoppingCart
            )

    @action(methods=['GET'], detail=False, url_path='download_shopping_cart')
    def get_download_shopping_cart(self, request):
        shopping_cart = request.user.shopping_cart.all()
        result_ingredients = create_shopping_dict(shopping_cart)
        create_shopping_cart_txt(result_ingredients)

        file_path = os.path.join(MEDIA_ROOT, 'shopping_cart.txt')

        if not os.path.exists(file_path):
            return Response({'error': 'Файл не найден'})

        return FileResponse(open(file_path, 'rb'), as_attachment=True,
                            filename='data.txt')


