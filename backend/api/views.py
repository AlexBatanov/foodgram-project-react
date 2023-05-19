from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для просмотра и редактирования
    для рецептов. 
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()