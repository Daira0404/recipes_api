from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Recipe, CustomUser, Comment, UserRanking
from .serializers import UserSerializer, RecipeSerializer, RecipesUserSerializer, CommentSerializer, UserRankingSerializer, RecipeRankingSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from django.db.models import Avg

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        user = None
        if '@' in email:
            try:
                user = CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateRecipeView(CreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

class RecipesView(ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

class RecipesUserView(ListAPIView):
    serializer_class = RecipesUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

class CreateCommentsView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class CommentsOfRecipeView(RetrieveAPIView):
    serializer_class = CommentSerializer

    def get_object(self):
        recipe_id = self.kwargs.get('pk')
        return Recipe.objects.get(pk=recipe_id)

    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()
        comments = recipe.comment_set.all()
        comments_serializer = CommentSerializer(comments, many=True)
        return Response(comments_serializer.data)

class AllRecipeAndCommentsView(ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        comments = Comment.objects.all()
        comments_serializer = CommentSerializer(comments, many=True)

        comments_for_recipe = {}
        for comment in comments:
            recipe_id = comment.recipe_id
            if recipe_id not in comments_for_recipe:
                comments_for_recipe[recipe_id] = []
            comments_for_recipe[recipe_id].append(comment)

        data = serializer.data
        for recipe_data in data:
            recipe_id = recipe_data['id']
            if recipe_id in comments_for_recipe:
                recipe_data['comments'] = CommentSerializer(comments_for_recipe[recipe_id], many=True).data
            else:
                recipe_data['comments'] = []

        return Response(data)

class CreateRankingView(CreateAPIView):
    serializer_class = UserRankingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Obtener la receta y el usuario actual
            recipe_id = serializer.validated_data['recipe'].id
            user = self.request.user

            # Verificar si el usuario ya ha calificado esta receta
            if UserRanking.objects.filter(recipe_id=recipe_id, user=user).exists():
                return Response({'error': 'El usuario ya ha calificado esta receta.'}, status=status.HTTP_400_BAD_REQUEST)

            # Guardar la calificación
            serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RankingOfRecipeView(RetrieveAPIView):
    serializer_class = RecipeRankingSerializer

    def get_object(self):
        recipe_id = self.kwargs.get('pk')
        recipe = Recipe.objects.get(pk=recipe_id)
        ranking = UserRanking.objects.filter(recipe=recipe).aggregate(Avg('ranking'))['ranking__avg']
        
        # Crear un diccionario que contenga la receta y el ranking
        recipe_data = {
            'recipe': recipe,  # Asegúrate de que recipe sea un objeto Recipe
            'ranking': ranking,
        }
        
        return recipe_data

class AllRecipesWithRankingsView(ListAPIView):
    serializer_class = RecipeRankingSerializer

    def get_queryset(self):
        # Obtener las recetas y calcular los promedios de calificaciones
        recipes = Recipe.objects.all()
        rankings = UserRanking.objects.filter(recipe__in=recipes).values('recipe').annotate(ranking=Avg('ranking'))

        # Combinar recetas con sus rankings calculados
        recipes_with_rankings = [{'recipe': recipe, 'ranking': ranking['ranking']} for recipe, ranking in zip(recipes, rankings)]

        return recipes_with_rankings