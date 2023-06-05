from rest_framework import viewsets, filters

from .serializers import IngredientSerializer
from .models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Набор представлений для просмотра рецептов
    Реализована фильтрация по названию
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        search_term = self.request.query_params.get('name', None)
        if search_term:
            queryset = queryset.filter(name__startswith=search_term) | queryset.filter(name__icontains=search_term)
        return queryset