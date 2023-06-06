from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для отображения тегов
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
