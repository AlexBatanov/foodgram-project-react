from django.shortcuts import get_object_or_404
from rest_framework import serializers

from tags.serializers import TagSerializer
from users.serializers import UserSubscribedSerializer
from .models import Recipe
from favorites_shop.models import Favorites
from favorites_shop.models import ShoppingCart
from .helpers import chek_is_favorite_and_is_shoping_list
from ingredients.models import Ingredient
from .models import RecipeIngredient


    
class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов рецепта"""

    name = serializers.CharField(source='ingredient.name', read_only=True)
    quantity = serializers.IntegerField(source='ingredient.quantity', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'measurement_unit', 'amount']

class RecipeSerializer(serializers.ModelSerializer):
    """Сериалазер для создания и отображения рецептов"""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
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

class CreateRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        recipe = Recipe.objects.create(**validated_data)
        ingredients = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.pop('id', None)
            if ingredient_id:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                ingredients.append(RecipeIngredient(recipe=recipe, ingredient=ingredient, **ingredient_data))
        RecipeIngredient.objects.bulk_create(ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        instance = super().update(instance, validated_data)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id', None)
            if ingredient_id:
                ingredient = RecipeIngredient.objects.get(id=ingredient_id, recipe=instance)
                ingredient.amount = ingredient_data.get('amount', ingredient.amount)
                ingredient.save()
            else:
                RecipeIngredient.objects.create(recipe=instance, **ingredient_data)
        return instance
