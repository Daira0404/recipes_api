from django.urls import path, include
from recipes import views
from .views import register_user, user_login, user_logout, CommentsOfRecipeView, AllRecipeAndCommentsView, RankingOfRecipeView, AllRecipesWithRankingsView
urlpatterns = [
    path('register/', register_user),
    path('login/', user_login),
    path('logout/', user_logout),
    path('recipe/create/', views.CreateRecipeView.as_view()),
    path('recipes/', views.RecipesView.as_view()),
    path('recipe_user/', views.RecipesUserView.as_view()),
    path('create_comment/', views.CreateCommentsView.as_view()),
    path('comments_recipe/<int:pk>/', CommentsOfRecipeView.as_view()),
    path('all_recipes_and_comments/', AllRecipeAndCommentsView.as_view()),
    path('add_ranking/', views.CreateRankingView.as_view()),
    path('ranking_recipe/<int:pk>/', RankingOfRecipeView.as_view()),
    path('all_recipes_and_ranking/', AllRecipesWithRankingsView.as_view()),

]