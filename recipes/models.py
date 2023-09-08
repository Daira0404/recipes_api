from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=150, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']
    rated_recipes = models.ManyToManyField('Recipe', through='UserRanking')

class Category(models.Model):
    name = models.CharField(max_length=100)

class Method(models.Model):
    name = models.CharField(max_length=100, default="")

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instruccions = models.TextField()
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField('Ingredient', through='IngredientRecipe')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    method = models.ForeignKey(Method, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="recipe", null=True)
    def __str__(self):
        return self.titulo

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)
    measure = models.CharField(max_length=50)
    
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class UserRanking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ranking = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="La calificación mínima es 1."),
            MaxValueValidator(5, message="La calificación máxima es 5.")
        ]
    )

    class Meta:
        unique_together = ('user', 'recipe')