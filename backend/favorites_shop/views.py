from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from .serializers import RecepeFavoritShopSerializer
from .models import Favorites, ShoppingCart
from .helpers import add_recipe_in_card_favorite

User = get_user_model()


class FavoritesView(viewsets.ViewSet):

    permission_classes = [IsAuthenticated,]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='favorite')
    def favorites_add(self, request, pk):
        return add_recipe_in_card_favorite(request=request, pk=pk, serializer=RecepeFavoritShopSerializer, model=Favorites)


class ShoppingCardView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]

    @action(methods=['POST', 'DELETE'], detail=True, url_path='shopping_cart')
    def shopping_card_add(self, request, pk):
        return add_recipe_in_card_favorite(request=request, pk=pk, serializer=RecepeFavoritShopSerializer, model=ShoppingCart)

    @action(methods=['GET'], detail=False, url_path='download_shopping_cart')
    def get_download_shopping_cart(self, request):
        recipes = ShoppingCart.objects.filter(user=request.user)
        serializer = RecepeFavoritShopSerializer(recipes, many=True)
        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)

