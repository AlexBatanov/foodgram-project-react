from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Recipe
from .serializers import RecipeSerializer, RecipeCreateSerializer
from .helpers import cheking_ownership
from .filters import FilterRecipes


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и
    редактирования рецептов. 
    """

    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterRecipes

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        if self.request.method == 'PATCH':
            cheking_ownership(self, self.get_object())
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        cheking_ownership(self, instance)
        return super().perform_destroy(instance)


    