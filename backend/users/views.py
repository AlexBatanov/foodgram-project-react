from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer, TokenSerializer, SetPasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Реализация CRUD для пользователей.
    переопределены методы получения, обновления и удаления,
    для работы со своим профилем исходя из требований.
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TokenLoginViewSet(APIView):
    """Если уже есть токен вызывается исключение - нужно исправить"""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, email=serializer.data.get('email'))

        if user.check_password(serializer.data.get('password')):
            token = Token.objects.create(user=user)
            return Response({"auth_token": token.key})
        return Response(data='Не верный пароль', status=status.HTTP_400_BAD_REQUEST)
    
class TokenLogautViewSet(APIView):
    def post(self, request):
        try:
            user_token = Token.objects.get(user=request.user)
            user_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('data: Пользователь не авторизован', status=status.HTTP_401_UNAUTHORIZED)

class SetPasswordViewSet(APIView):
    def post(self, request):
        user = request.user
        serializer = SetPasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(data='Пароль изменен', status=status.HTTP_200_OK)