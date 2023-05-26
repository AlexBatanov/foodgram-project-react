from rest_framework import viewsets

from .serializers import IngredientSerializer
from .models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)
