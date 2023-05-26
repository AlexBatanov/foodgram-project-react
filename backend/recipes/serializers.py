from rest_framework import serializers

from tags.serializers import TagSerializer
from ingredients.serializers import IngredientSerializer
from users.serializers import UserSubscribedSerializer
from .models import Recipe
from favorites_shop.models import Favorites


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True)
    author = UserSubscribedSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited', 'name', 'image', 'text', 'cooking_time']

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Favorites.objects.filter(recipe=obj, user=user).exists()
