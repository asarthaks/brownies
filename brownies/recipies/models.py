from django.db import models

# Create your models here.
<<<<<<< HEAD
=======
from django.db import models
from django.contrib.auth.models import User

class Dish(models.Model):
    dish_name = models.CharField(max_length = 180)
    recipe = models.CharField(max_length = 600)
    completed = models.BooleanField(default = False, blank = True)
    updated = models.DateTimeField(auto_now = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.dish_name

class DishIngredient(models.Model):
    ingredient_name = models.CharField(max_length = 100)
    ingredient_amount = models.CharField(max_length = 10)
    ingredient_unit = models.CharField(max_length = 20)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.ingredient_name
>>>>>>> b0dd2b2 (access part)
