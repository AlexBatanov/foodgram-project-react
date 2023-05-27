from rest_framework import serializers

from tags.serializers import TagSerializer
from ingredients.serializers import IngredientSerializer
from users.serializers import UserSubscribedSerializer
from .models import Recipe
from favorites_shop.models import Favorites
from favorites_shop.models import ShoppingCart
from .helpers import chek_is_favorite_and_is_shoping_list


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалазер для создания и отображения рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True)
    author = UserSubscribedSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time']

    def get_is_favorited(self, obj):
        return chek_is_favorite_and_is_shoping_list(
            context=self.context,
            obj=obj,
            model=Favorites
        )

    def get_is_in_shopping_cart(self, obj):
        return chek_is_favorite_and_is_shoping_list(
            context=self.context,
            obj=obj,
            model=ShoppingCart
        )