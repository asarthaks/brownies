import requests
from bs4 import BeautifulSoup
from lxml import etree
import cloudscraper


def scrape_ingredients(dom):
    xpath_str = '//ul[@class="wprm-recipe-ingredients"]/li'
    ingredients_list = list()
    for item in dom.xpath(xpath_str):
        # print(item)
        ingredient_dict = dict()
        ingredient_contents = item.xpath("span")
        # print(ingredient_contents)
        for ingredient_content in ingredient_contents:
            ingredient_content_type = ingredient_content.xpath("@class")[0]
            # print(ingredient_content_type)
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
    xpath_str = '//div[@class="wprm-recipe-instruction-text"]'
    recipe = ""
    for idx, div in enumerate(dom.xpath(xpath_str)):
        step_text = "{}) ".format(idx+1)
        for steps in div.itertext():
            step_text += steps
        recipe += step_text + "\n"
    return recipe

def scrape_complete_recipe(dish_name):
    content = scraper.get("https://tastesbetterfromscratch.com/{}/".format(dish_name)).text
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find("body")
    dom = etree.HTML(str(body)) # Parse the HTML content of the page
    ingredients_list = scrape_ingredients(dom)
    pprint(ingredients_list)
    recipe = scrape_recipe(dom)
    print(recipe)


def scrape_and_return_dish(dish_name):
    content = scraper.get("https://tastesbetterfromscratch.com/{}/".format(dish_name)).text
    soup = BeautifulSoup(content, 'html.parser')
    body = soup.find("body")
    dom = etree.HTML(str(body)) # Parse the HTML content of the page
    ingredients_list = scrape_ingredients(dom)
    recipe = scrape_recipe(dom)
    return {"ingredients": ingredients_list, "recipe": recipe}  



def prepare_list_of_dishes(dom):
    dish_list = list()
    for item in dom.xpath('//h3["@class=post-summary__title"]'):
        dish_list.append(item.xpath("a")[0].values()[0].split('/')[-2])

    for item in dom.xpath('//h2["@class=post-summary__title"]'):
        if item.getchildren():
            if "meal-plan" not in item.xpath("a")[0].values()[0]:
                dish_list.append(item.xpath("a")[0].values()[0].split('/')[-2])

    return dish_list

scraper = cloudscraper.create_scraper()
content = scraper.get("https://tastesbetterfromscratch.com/recipe-index/").text
soup = BeautifulSoup(content, 'html.parser')
body = soup.find("body")
dom = etree.HTML(str(body)) # Parse the HTML content of the page



