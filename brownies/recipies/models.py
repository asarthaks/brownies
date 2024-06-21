from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    dish_name = models.CharField(max_length = 180, unique=True)
    recipe = models.CharField(max_length = 2000)

    def __str__(self):
        return self.dish_name

class DishIngredient(models.Model):
    ingredient_name = models.CharField(max_length = 100, null=False)
    ingredient_amount = models.CharField(max_length = 10)
    ingredient_unit = models.CharField(max_length = 20)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.ingredient_name
