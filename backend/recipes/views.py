from rest_framework import viewsets

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и редактирования
    для рецептов. 
    """
    # serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer