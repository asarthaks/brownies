from django.contrib import admin
from .models import Dish, DishIngredient

admin.site.register(Dish)
admin.site.register(DishIngredient)
