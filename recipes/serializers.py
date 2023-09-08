from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser, Recipe, Comment, UserRanking

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRanking
        fields = '__all__'

class RecipeRankingSerializer(serializers.Serializer):
    recipe = RecipeSerializer()  # Usar tu serializador Recipe para la receta
    ranking = serializers.DecimalField(max_digits=3, decimal_places=2)