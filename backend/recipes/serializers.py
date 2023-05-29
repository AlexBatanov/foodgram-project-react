from rest_framework import serializers

from tags.serializers import TagSerializer
from users.serializers import UserSubscribedSerializer
from .models import Recipe
from favorites_shop.models import Favorites
from favorites_shop.models import ShoppingCart
from .helpers import chek_is_favorite_and_is_shoping_list, creat_ingredients
from .models import RecipeIngredient


    
class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения ингредиентов рецепта"""

    name = serializers.CharField(source='ingredient.name', read_only=True)
    quantity = serializers.IntegerField(source='ingredient.quantity', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'measurement_unit', 'amount']


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания связи ингрединта и количества"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалазер для отображения рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
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


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания и обновления рецептов"""

    ingredients = IngredientAmountCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'name', 'image', 'text', 'cooking_time']

    def create(self, data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        ingredients_list = creat_ingredients(ingredients)
        recipe = Recipe.objects.create(**data)
        recipe.ingredients.set(ingredients_list)
        recipe.tags.set(tags)

        return recipe
    
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

