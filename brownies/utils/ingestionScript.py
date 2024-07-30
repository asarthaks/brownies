import time
import psycopg2

class PostgresConnection:
    """
    A context manager class to handle PostgreSQL database connections.
    
    Attributes:
        hostname (str): The hostname of the PostgreSQL server.
        port (str): The port number on which the PostgreSQL server is running.
        dbname (str): The name of the PostgreSQL database.
        username (str): The username to connect to the PostgreSQL database.
        password (str): The password to connect to the PostgreSQL database.
        conn (psycopg2.connection): The PostgreSQL connection object.
        cur (psycopg2.cursor): The PostgreSQL cursor object.
    """
    def __init__(self, hostname, port, dbname, username, password):
        self.hostname = hostname
        self.port = port
        self.dbname = dbname
        self.username = username
        self.password = password
        self.conn = None
        self.cur = None

    def __enter__(self):
        """
        Establish a database connection and return a cursor object.
        
        Returns:
            psycopg2.cursor: The PostgreSQL cursor object.
        """
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
        """
        Close the cursor and the connection when exiting the context.
        """
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print("Connection closed")

class Dish:
    """
    A class to represent a dish and manage its database operations.
    
    Attributes:
        cursor (psycopg2.cursor): The PostgreSQL cursor object.
        id (int): The ID of the dish.
        dish_name (str): The name of the dish.
        recipe (str): The recipe of the dish.
    """
    def __init__(self, cursor, dish_name, recipe):
        select_sql = "SELECT max(id) FROM recipies_dish;"
        cursor.execute(select_sql)
        self.cursor = cursor
        self.id = cursor.fetchall()[0][0] + 1
        self.dish_name = dish_name
        self.recipe = recipe

    def save_to_db(self):
        """
        Save the dish details to the database.
        """
        insert_sql = """
        INSERT INTO recipies_dish (id, dish_name, recipe)
        VALUES (%s, %s, %s)
        ON CONFLICT (dish_name) DO NOTHING;
        """
        self.cursor.execute(insert_sql, (self.id, self.dish_name, self.recipe))

    @staticmethod
    def get_all(self):
        """
        Retrieve all dishes from the database.
        
        Args:
            cursor (psycopg2.cursor): The PostgreSQL cursor object.
        
        Returns:
            list: A list of all dishes.
        """
        select_sql = "SELECT * FROM recipies_dish;"
        self.cursor.execute(select_sql)
        return cursor.fetchall()


    @staticmethod
    def get_by_name(self, dish_name):
        """
        Retrieve a dish by its name from the database.
        
        Args:
            cursor (psycopg2.cursor): The PostgreSQL cursor object.
            dish_name (str): The name of the dish.
        
        Returns:
            list: A list of dishes that match the given name.
        """
        select_sql = "SELECT * FROM recipies_dish WHERE dish_name = %s;"
        self.cursor.execute(select_sql, (dish_name,))
        return cursor.fetchall()
    
    @staticmethod
    def get_by_id(self, dish_id):
        """
        Retrieve a dish by its ID from the database.
        
        Args:
            cursor (psycopg2.cursor): The PostgreSQL cursor object.
            dish_id (int): The ID of the dish.
        
        Returns:
            list: A list of dishes that match the given ID.
        """
        select_sql = "SELECT * FROM recipies_dish WHERE id = %s;"
        self.cursor.execute(select_sql, (dish_id,))
        return cursor.fetchall()

class DishIngredient:
    """
    A class to represent a dish ingredient and manage its database operations.
    
    Attributes:
        cursor (psycopg2.cursor): The PostgreSQL cursor object.
        id (int): The ID of the ingredient.
        name (str): The name of the ingredient.
        amount (str): The amount of the ingredient.
        unit (str): The unit of the ingredient amount.
        dish_id (int): The ID of the dish to which the ingredient belongs.
    """
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
        """
        Save the ingredient details to the database.
        """
        insert_sql = """
        INSERT INTO recipies_dishingredient (id, ingredient_name, ingredient_amount, ingredient_unit, dish_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        self.cursor.execute(insert_sql, (self.id, self.name, self.amount, self.unit, self.dish_id))

    @staticmethod
    def get_all(self):
        """
        Retrieve all ingredients from the database.
        
        Args:
            cursor (psycopg2.cursor): The PostgreSQL cursor object.
        
        Returns:
            list: A list of all ingredients.
        """
        select_sql = "SELECT * FROM recipies_dishingredient;"
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()

# Import the scraper script
from scraperScript import *

# Prepare the list of dishes using the scraper script
dish_list = prepare_list_of_dishes(dom)

# Database connection parameters
hostname = 'brownies-server-postgres'
port = '5432'
dbname = 'postgres'
username = 'postgres'
password = 'brownies_db'

# Establish a database connection
conn = psycopg2.connect(
    dbname=dbname,
    user=username,
    password=password,
    host=hostname,  
    port=port
)

# Create a cursor object
cur = conn.cursor()

# Process and store each dish and its ingredients
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
        # Uncomment the line below to save ingredients to the database
        ingredient_obj.save_to_db()
    print("Done")
    # Optional delay to prevent overloading the server
    # time.sleep(0.5)

# Commit the transaction to the database
# conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
