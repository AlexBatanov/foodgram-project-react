from rest_framework import serializers

from recipes.models import Recipe


class RecepeFavoritShopSerializer(serializers.ModelSerializer):
    """Сериалазер для отображения рецептов в избранном"""

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
