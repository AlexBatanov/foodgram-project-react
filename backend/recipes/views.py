from rest_framework import viewsets

from .models import Recipe
from .serializers import RecipeSerializer, RecipeCreateSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и редактирования
    для рецептов. 
    """

    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        
        if self.request.method in ['POST', 'DELETE']:
            return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)