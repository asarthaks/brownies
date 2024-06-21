from django.shortcuts import render

# Create your views here.
 
def index(request):
    context = {
        'title': 'Hello, Jinja in Django!', 
        'user_authenticated': True, 
        'username': 'Brownies', 
        'items': ['Dishes', 'Dish Ingredients', 'Python', 'Javascript']
    }
    return render(request, 'index.html', context)
