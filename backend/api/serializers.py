import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Recipe, Tag, User, Ingredient


class AuthSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'длина email должна быть меньше 254 символов')
        return value

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username не может быть me')

        if not re.match(r'[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'поле username должно состоять из латинских букв и цифр')

        if len(value) > 150:
            raise serializers.ValidationError(
                'длина username должна быть меньше 150 символов')
        return value
    
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'password', ]

    def get_is_subscribed(self, obj):
        # print(obj.__dict__)
        if not self.context.get('request'):
            return False
        user = self.context['request'].user
        return user.is_authenticated and user in obj.subscribers.all()
    
    # def validate_email(self, value):
    #     if len(value) > 254:
    #         raise serializers.ValidationError(
    #             'длина email должна быть меньше 254 символов')
    #     return value

    # def validate_username(self, value):
    #     if value == 'me':
    #         raise serializers.ValidationError('username не может быть me')

    #     if not re.match(r'[\w.@+-]+\Z', value):
    #         raise serializers.ValidationError(
    #             'поле username должно состоять из латинских букв и цифр')

    #     if len(value) > 150:
    #         raise serializers.ValidationError(
    #             'длина username должна быть меньше 150 символов')
    #     return value
    
    def create(self, validated_data):
        user = super().create(validated_data)
        # user.set_password(validated_data['password'])
        user.save()
        return user

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = '__all__'
