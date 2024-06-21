import time
import psycopg2


class PostgresConnection:
    def __init__(self, hostname, port, dbname, username, password):
        self.hostname = hostname
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.conn = None
        self.cur = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self.hostname,
                port=self.port,
                dbname=self.dbname,
                user=self.username,
                password=self.password
            )
            print("Connection successful")
            self.cur = self.conn.cursor()
            return self.cur  # Return the cursor object
        except Exception as error:
            print(f"Error: {error}")
            if self.conn:
                self.conn.close()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure the cursor and connection are closed
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print("Connection closed")

class Dish:
    def __init__(self, cursor, dish_name, recipe):
        select_sql = "SELECT max(id) FROM recipies_dish;"
        cursor.execute(select_sql)
        self.cursor = cursor
        self.id = cursor.fetchall()[0][0] + 1
        self.dish_name = dish_name
        self.recipe = recipe

    def save_to_db(self):
        insert_sql = """
        INSERT INTO recipies_dish (id, dish_name, recipe)
        VALUES (%s, %s, %s)
        ON CONFLICT (dish_name) DO NOTHING;
        """
        self.cursor.execute(insert_sql, (self.id, self.dish_name, self.recipe))

    @staticmethod
    def get_all(self):
        select_sql = "SELECT * FROM recipies_dish;"
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()
    
    @staticmethod
    def get_by_name(self, dish_name):
        select_sql = "SELECT * FROM recipies_dish WHERE dish_name = %s;"
        self.cursor.execute(select_sql, (dish_name,))
        return self.cursor.fetchall()
    
    @staticmethod
    def get_by_id(self, dish_id):
        select_sql = "SELECT * FROM recipies_dish WHERE id = %s;"
        self.cursor.execute(select_sql, (dish_id,))
        return self.cursor.fetchall()

class DishIngredient:
    def __init__(self, cursor, name, amount, unit, dish_id):
        select_sql = "SELECT max(id) FROM recipies_dishingredient;"
        cursor.execute(select_sql)
        self.cursor = cursor
        self.id = cursor.fetchall()[0][0] + 1
        self.name = name
        self.amount = amount
        self.unit = unit
        self.dish_id = dish_id

    def save_to_db(self):
        insert_sql = """
        INSERT INTO recipies_dishingredient (id, ingredient_name, ingredient_amount, ingredient_unit, dish_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        self.cursor.execute(insert_sql, (self.id, self.name, self.amount, self.unit, self.dish_id))

    @staticmethod
    def get_all(self):
        select_sql = "SELECT * FROM recipies_dishingredient;"
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()

from scraperScript import *

#Imported

dish_list = prepare_list_of_dishes(dom)

# Example usage
hostname = 'brownies-server-postgres'
port = '5432'
dbname = 'postgres'
username = 'postgres'
password = 'brownies_db'

conn = psycopg2.connect(
    dbname=dbname,
    user=username,
    password=password,
    host=hostname,  
    port=port
)

cur = conn.cursor()


unique_dishes = set(dish_list)
for dish in dish_list:
    print("Scraping the Dish: {}".format(dish))
    dish_data = scrape_and_return_dish(dish)
    dish_obj = Dish(cur, dish, dish_data["recipe"])
    dish_obj.save_to_db()
    print("Ingesting the recipe and ingredients for {} into the Database!".format(dish))
    for ingredient in dish_data["ingredients"]:
        ingredient_name = ingredient["ingredient_name"]
        ingredient_amount = ingredient.get("ingredient_amount", "")
        ingredient_unit = ingredient.get("ingredient_unit", "")
        ingredient_obj = DishIngredient(cur, ingredient_name, ingredient_amount, ingredient_unit, dish_obj.id)
        ingredient_obj.__dict__.pop("cursor")
        ingredient_obj.__dict__.pop("id")
        ingredient_obj.__dict__.pop("dish_id")
        print("\t", ingredient_obj.__dict__)
        # ingredient_obj.save_to_db()
    print("Done")
    # time.sleep(0.5)

# Commit the transaction
# conn.commit()

# Close the cursor and connection
cur.close()
conn.close()