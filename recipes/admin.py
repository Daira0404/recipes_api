from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Recipe, Category, Method, Ingredient, IngredientRecipe

@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    pass

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientRecipe)
admin.site.register(Category)
admin.site.register(Method)