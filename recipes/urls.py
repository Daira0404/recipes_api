from django.urls import path, include
from recipes import views
from .views import register_user, user_login, user_logout

urlpatterns = [
    path('register/', register_user),
    path('login/', user_login),
    path('logout/', user_logout),
    path('recipe/create/', views.CreateRecipeView.as_view()),
    path('recipes/', views.RecipesView.as_view()),
    path('recipe_user/', views.RecipesUserView.as_view()),
    #path('create_comment/', views.CreateCommentView.as_view()),
    #path('add_ranking/', views.AddRankingView.as_view()),
]