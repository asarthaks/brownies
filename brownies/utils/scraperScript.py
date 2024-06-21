import requests
from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper
from pprint import pprint


def scrape_ingredients(dom):
    """
    Scrape ingredients from the DOM.
    
    Args:
        dom: The DOM object representing the HTML structure of the page.
    
    Returns:
        A list of dictionaries, each containing ingredient details.
    """
    xpath_str = '//ul[@class="wprm-recipe-ingredients"]/li'
    ingredients_list = []
    
    for item in dom.xpath(xpath_str):
        ingredient_dict = {}
        ingredient_contents = item.xpath("span")
        
        for ingredient_content in ingredient_contents:
            ingredient_content_type = ingredient_content.xpath("@class")[0]
            
            if ingredient_content_type == "wprm-recipe-ingredient-name":
                if ingredient_content.text:
                    ingredient_name = ingredient_content.text
                else:
                    ingredient_name = ingredient_content.xpath("*")[0].text
                ingredient_dict["ingredient_name"] = ingredient_name
            
            elif ingredient_content_type == "wprm-recipe-ingredient-unit":
                ingredient_unit = ingredient_content.text
                ingredient_dict["ingredient_unit"] = ingredient_unit
            
            elif ingredient_content_type == "wprm-recipe-ingredient-amount":
                ingredient_amount = ingredient_content.text
                ingredient_dict["ingredient_amount"] = ingredient_amount
        
        ingredients_list.append(ingredient_dict)
    
    return ingredients_list


def scrape_recipe(dom):
    """
    Scrape recipe steps from the DOM.
    
    Args:
        dom: The DOM object representing the HTML structure of the page.
    
    Returns:
        A string representing the full recipe with steps.
    """
    xpath_str = '//div[@class="wprm-recipe-instruction-text"]'
    recipe = ""
    
    for idx, div in enumerate(dom.xpath(xpath_str)):
        step_text = "{}. ".format(idx + 1)
        
        for steps in div.itertext():
            step_text += steps
        
        recipe += step_text + "\n"
    
    return recipe


def scrape_complete_recipe(dish_name):
    """
    Scrape the complete recipe for a given dish name.
    
    Args:
        dish_name: The name of the dish to scrape.
    """
    content = scraper.get("https://tastesbetterfromscratch.com/{}/".format(dish_name)).text
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find("body")
    dom = etree.HTML(str(body))  # Parse the HTML content of the page
    
    ingredients_list = scrape_ingredients(dom)
    pprint(ingredients_list)
    
    recipe = scrape_recipe(dom)
    print(recipe)


def scrape_and_return_dish(dish_name):
    """
    Scrape and return the complete recipe and ingredients for a given dish name.
    
    Args:
        dish_name: The name of the dish to scrape.
    
    Returns:
        A dictionary containing the ingredients list and the recipe.
    """
    content = scraper.get("https://tastesbetterfromscratch.com/{}/".format(dish_name)).text
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find("body")
    dom = etree.HTML(str(body))  # Parse the HTML content of the page
    
    ingredients_list = scrape_ingredients(dom)
    recipe = scrape_recipe(dom)
    
    return {"ingredients": ingredients_list, "recipe": recipe}


def prepare_list_of_dishes(dom):
    """
    Prepare a list of dish names from the DOM.
    
    Args:
        dom: The DOM object representing the HTML structure of the page.
    
    Returns:
        A list of dish names.
    """
    dish_list = []
    
    # Extract dish names from <h3> elements
    for item in dom.xpath('//h3[@class="post-summary__title"]'):
        dish_list.append(item.xpath("a")[0].values()[0].split('/')[-2])
    
    # Extract dish names from <h2> elements, excluding meal plans
    for item in dom.xpath('//h2[@class="post-summary__title"]'):
        if item.getchildren():
            if "meal-plan" not in item.xpath("a")[0].values()[0]:
                dish_list.append(item.xpath("a")[0].values()[0].split('/')[-2])
    
    return dish_list

# Create a cloudscraper instance to bypass Cloudflare's security measures
scraper = cloudscraper.create_scraper()

# Get the HTML content from the recipe index page
content = scraper.get("https://tastesbetterfromscratch.com/recipe-index/").text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Find the <body> element in the parsed HTML
body = soup.find("body")

# Convert the <body> element into an lxml DOM object
dom = etree.HTML(str(body))
