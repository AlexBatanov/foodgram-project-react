from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from favorites_shop.serializers import RecepeFavoritShopSerializer
from .models import Subscription


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания пользователя
    отображения пользователя после регистрации
    """

    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email
    
    def save(self, **kwargs):
        password = self.validated_data.pop('password')
        user, _ = User.objects.get_or_create(**self.validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def get_id(self, obj):
        return User.objects.get(email=obj.get('email')).id
    
class UserSubscribedSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения всех пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):

        if not self.context.get('request'):
            return False
        user = self.context['request'].user
        return user.is_authenticated and Subscription.objects.filter(user=user, author=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения пользователей на которых подписан"""

    is_subscribed = serializers.BooleanField(default=True)
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count']

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        return RecepeFavoritShopSerializer(recipes, many=True).data
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
