from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

## Utility functions for running queries, getting relevant dish and ingredients

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_dish_from_ingredient(ingredient_name):
    """
    Retrieve dishes that contain the given ingredient name.
    """
    cursor = connection.cursor()
    query = """
        SELECT dish_id, dish_name, ingredient_name, ingredient_amount, ingredient_unit
        FROM recipies_dishingredient A
        LEFT OUTER JOIN recipies_dish B ON A.dish_id = B.id
        WHERE ingredient_name LIKE %s
    """
    cursor.execute(query, ['%' + ingredient_name + '%'])
    data = dictfetchall(cursor)
    return data

def get_complete_recipe(dish_id):
    """
    Retrieve the complete recipe for a given dish ID.
    """
    cursor = connection.cursor()
    query = """
        SELECT json_agg(
                json_build_object(
                    'dish_name', d.dish_name,
                    'recipe', d.recipe,
                    'ingredients', (
                        SELECT json_agg(
                            json_build_object(
                                'ingredient_name', di.ingredient_name,
                                'ingredient_amount', di.ingredient_amount,
                                'ingredient_unit', di.ingredient_unit
                            )
                        )
                        FROM recipies_dishingredient di
                        WHERE di.dish_id = d.id
                    )
                )
            ) AS recipes
        FROM recipies_dish d
        WHERE d.id = %s;
    """
    cursor.execute(query, [dish_id])
    data = dictfetchall(cursor)
    return data

## Functions for the APIs

def search(request):
    """
    Handle search requests to find dishes by ingredient.
    """
    context = {}
    
    # Check if there is a query input
    if request.GET.get('query_input'):
        # Prepare context based on the input
        context["search"] = request.GET.get('search_button')
        context["query"] = request.GET.get('query_input')
        
        # Use utility function to get relevant dishes from the input ingredient
        results = get_dish_from_ingredient(context["query"])
        context["items"] = results
    
    # Render the results
    return render(request, 'RecipeSearchTemplate.html', context)

def recipe(request):
    """
    Handle requests to fetch and display a complete recipe by dish ID.
    """
    context = {}
    
    # Fetch the complete recipe by the given dish ID
    dish_id = request.GET.get('dish_id')
    complete_recipe = get_complete_recipe(dish_id)
    
    # Assuming there is only one recipe in the response
    context = complete_recipe[0]["recipes"][0]
    
    # Render the results
    return render(request, 'RecipeSearchTemplate.html', context)
