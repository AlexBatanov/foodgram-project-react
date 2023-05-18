from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Recipe, Tag, Ingredient, User
from .serializers import AuthSerializer, RecipeSerializer, UserSerializer, TokenSerializer
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

class TokenViewSet(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, email=serializer.data.get('email'))

        if user.check_password(serializer.data.get('password')):
            return Response({"auth_token": "string"})
        return Response(data='Не верный пароль', status=status.HTTP_400_BAD_REQUEST)