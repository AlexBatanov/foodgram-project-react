from rest_framework import serializers

from recipes.models import Recipe


class RecepeFavoritShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']