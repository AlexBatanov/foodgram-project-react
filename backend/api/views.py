from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Recipe, Tag
from .serializers import RecipeSerializer, TagSerializer
from users.models import User


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

    def get_queryset(self):
        queryset = super().get_queryset()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        author_id = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')
        
        if is_favorited:
            queryset = queryset.filter(favorites__user=self.request.user)
        
        if is_in_shopping_cart:
            queryset = queryset.filter(shopping_list_items__user=self.request.user)
        
        if author_id:
            queryset = queryset.filter(author=get_object_or_404(User, id=author_id))
        
        if tags:
            queryset = queryset.filter(tags__name__in=tags)

        
        return queryset
