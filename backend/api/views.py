from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Recipe, Tag, Ingredient, User
from .serializers import AuthSerializer, RecipeSerializer, UserSerializer
from .helpers import get_users, send_massege


class UserViewSet(viewsets.ModelViewSet):
    """
    Реализация CRUD для пользователей.
    переопределены методы получения, обновления и удаления,
    для работы со своим профилем исходя из требований.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и редактирования
    для рецептов. 
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


