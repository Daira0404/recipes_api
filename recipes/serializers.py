from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser, Recipe

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class RecipesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


