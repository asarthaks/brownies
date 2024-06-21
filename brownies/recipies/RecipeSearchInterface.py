from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def get_dish_from_ingredient(ingredient_name):
    cursor = connection.cursor()
    query = "SELECT dish_id, dish_name, ingredient_name, ingredient_amount, ingredient_unit \
         FROM recipies_dishingredient A LEFT OUTER JOIN recipies_dish B ON A.dish_id = B.id \
         WHERE ingredient_name LIKE '%{}%'".format(ingredient_name)
    cursor.execute(query)
    data = dictfetchall(cursor)
    return data

def get_complete_recipe(dish_id):
    cursor = connection.cursor()
    query = """SELECT json_agg(
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
            WHERE d.id={};""".format(dish_id)
    cursor.execute(query)
    data = dictfetchall(cursor)
    return data




def search(request):
    context = dict()
    if request.GET.get('query_input'):
        context["search"] = request.GET.get('search_button')
        context["query"] = request.GET.get('query_input')
        results = get_dish_from_ingredient(context["query"])
        
        context["items"] = results
        print(results)
        a = get_complete_recipe(1)
        print(a)

    return render(request, 'RecipeSearchTemplate.html', context)

def recipe(request):
    context = dict()
    if request.GET.get('query_input'):
        context["search"] = request.GET.get('search_button')
        context["query"] = request.GET.get('query_input')
        results = get_dish_from_ingredient(context["query"])
        
        context["items"] = results
        print(results)
        a = get_complete_recipe(1)
        print(a)

    return render(request, 'RecipeSearchTemplate.html', context)

