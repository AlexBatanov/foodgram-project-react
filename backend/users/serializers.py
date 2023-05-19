import re

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation

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
    
class TokenSerializer(serializers.Serializer):
    """сделать поля обязательными для заполнения"""
    email = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True)

class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate(self, attrs):
        if attrs.get('new_password') == attrs.get('current_password'): #если два не верных пароля == тру - исправить
            raise serializers.ValidationError('Новый пароль похож на старый')
        return attrs
    
    def update(self, instance, validated_data):
        print(instance.check_password(validated_data.get('current_password')))
        if instance.check_password(validated_data.get('current_password')):
        # r = password_validation.validate_password(password=validated_data, instance=instance)
            instance.password = validated_data.get('new_password')
            instance.save()
            return instance
        raise serializers.ValidationError('Неверный пароль')

    #     if user.check_password(serializer.data.get('password')):
    #         token = Token.objects.create(user=user)
    #         return Response({"auth_token": token.key})
    #     return Response(data='Не верный пароль', status=status.HTTP_400_BAD_REQUEST)