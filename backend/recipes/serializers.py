from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from tags.serializers import TagSerializer
from users.serializers import UserSubscribedSerializer
from ingredients.models import Ingredient
from favorites_shop.models import Favorites, ShoppingCart
from .models import Recipe, RecipeIngredient
from .helpers import (chek_is_favorite_and_is_shoping_list,
                      creat_ingredients_return_tags)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения ингредиентов рецепта"""

    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    quantity = serializers.IntegerField(source='ingredient.quantity', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'quantity', 'measurement_unit', 'amount']


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания связи ингрединта и количества"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'amount']

    def validate_id(self, id):
        if not Ingredient.objects.filter(id=id).exists():
            raise serializers.ValidationError('Ингредиент не найден')
        return id

class RecipeSerializer(serializers.ModelSerializer):
    """Сериалазер для отображения рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    author = UserSubscribedSerializer(read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_favorited','is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time']

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
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['ingredients', 'tags', 'name', 'image', 'text', 'cooking_time']

    def create(self, data):
        ingredients, tags = creat_ingredients_return_tags(data)
        recipe = Recipe.objects.create(**data)
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags)

        return recipe

    def update(self, recipe, data):
        ingredients, tags = creat_ingredients_return_tags(data)
        recipe.ingredients.set(ingredients)
        recipe.tags.set(tags)

        return super().update(recipe, data)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

