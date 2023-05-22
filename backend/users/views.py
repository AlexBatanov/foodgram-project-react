from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from .serializers import SetPasswordSerializer, UserSubscribedSerializer, UsersSerializer
from .models import User

    
class UserViewSet(viewsets.ModelViewSet):
    """
    Реализация CRUD для пользователей.
    переопределены методы получения, обновления и удаления,
    для работы со своим профилем исходя из требований.
    """
    serializer_class = UserSubscribedSerializer, UsersSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_object(self):
        pk = self.request.parser_context['kwargs']['pk']

        if pk == 'me':
            instance = get_object_or_404(
                User,
                username=self.request.user.username
            )
        else:
            instance = get_object_or_404(User, pk=pk)

        return instance


    def partial_update(self, request, *args, **kwargs):

        if kwargs.get('pk') == 'me' and request.data.get('role'):
            return Response(
                {'error': 'нельзя изменять роль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        if kwargs.get('pk') == 'me':
            return Response(
                {'error': 'просите админа'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSubscribedSerializer
        return UsersSerializer
    
    @action(methods=['POST'], detail=False, url_path='set_password')
    def set_password(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            user = request.user
            password = serializer.validated_data.pop('new_password')
            user.set_password(password)
            user.save()

            return Response(data='Пароль изменен', status=status.HTTP_200_OK)
 
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
