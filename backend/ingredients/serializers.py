from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалазер для отображения ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
