from rest_framework import viewsets

from reviews.models import Recipe, Tag
from .serializers import RecipeSerializer, TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)

class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и редактирования
    для рецептов. 
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
