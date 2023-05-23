import re

from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Recipe, Tag, Ingredient
from users.models import User, Subscription


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'image', 'ciiking_time']

class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)

class UserSubscribedSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Subscription.objects.filter(author=obj, subscriber=user).exists()

class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
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
    
    def validate_password(self, value):
        validate_password(value)
        return value


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate(self, attrs):
        if self.context.get('user').check_password(attrs.get('current_password')):
            validate_password(attrs.get('new_password'))
            return attrs
        raise serializers.ValidationError('Неверный пароль')

class RecipeShortReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = RecipeShortReadSerializer(many=True)
    print('ok')
    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields + ['recipes']

    # def get_recipes(self):
    #     author = get_object_or_404(User, self.context.get('id'))
    #     if author and author != self.request.user:
    #         return author.get_recipe()
        # return serializers.ValidationError('Нет такого автора')
    
    # def get_author(self):
    #     return get_object_or_404(User, self.context.get('id'))

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    author = UserSubscribedSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'