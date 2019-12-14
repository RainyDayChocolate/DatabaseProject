import psycopg2
from data_structures import RecipeInstructions

class RestaurantData:

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM recipe LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def find_recipe(self, recipe_name):

        query_string = """select name from recipe
                          where name ~* %s
                        """
        cursor = self.conn.cursor()
        cursor.execute(query_string, (recipe_name,))
        qulified = cursor.fetchall()
        self.conn.commit()
        names = [{'name': name[0]} for name in qulified]

        return names

    def get_recipe_instructions(self, recipe_name):

        ingredient_query = """select name, amount
                                from
                                    recipe_ingredient
                                join
                                    ingredient
                                on recipe_ingredient.ingredient = ingredient.code
                                where recipe_ingredient.recipe = %s"""

        instruction_query = """select name, instructions from
                            recipe
                          where name = %s
                       """

        cursor = self.conn.cursor()

        cursor.execute(ingredient_query, (recipe_name, ))
        ingredients = cursor.fetchall()

        cursor.execute(instruction_query, (recipe_name, ))
        instructions = cursor.fetchall()
        name, instruction = instructions[0]
        self.conn.commit()
        return RecipeInstructions(name, instruction, ingredients)

    def get_seasonal_menu(self, season):
        season_kosher_query = """select recipe.name, kosher.is_kosher
                                from
                                    recipe
                                join
                                    (select recipe_ingredient.recipe,
                                            bool_and(is_kosher) as is_kosher
                                    from
                                        recipe_ingredient
                                    join
                                        ingredient
                                    on ingredient.code = recipe_ingredient.ingredient
                                    group by recipe_ingredient.recipe) kosher
                                on recipe.name = kosher.recipe
                                and (recipe.season = %s or recipe.season = $$All$$)
                              """
        cursor = self.conn.cursor()
        cursor.execute(season_kosher_query, (season, ))
        season_result = cursor.fetchall()
        self.conn.commit()
        return season_result

    def update_ingredient_price(self, ingredient_code, price):
        update_string = """WITH rows AS (
                            update ingredient
                            set cost_per_unit = %s
                            where ingredient.code = %s
                            returning 1)
                            SELECT count(*) FROM rows;
                        """
        cursor = self.conn.cursor()
        cursor.execute(update_string, (price, ingredient_code))
        (number_of_rows, )=cursor.fetchone()
        self.conn.commit()
        return number_of_rows

    def add_new_recipe(self, recipe_instructions, servings, course, season):
        ingredient_dectect_query = """select code from ingredient
                                        where name=%s
                                    """
        insert_recipe_ingredient_query = """Insert into recipe_ingredient
                                            (ingredient, recipe, amount)
                                            values(%s, %s, %s)
                                        """
        insert_recipe_query = """Insert into recipe
                                    (name, instructions, servings, course, season)
                                    values(%s, %s, %s, %s, %s)
                                """
        cursor = self.conn.cursor()

        ingredients, amounts = zip(*recipe_instructions.ingredients)
        instrutions = recipe_instructions.instructions
        name = recipe_instructions.name
        codes = []
        for ingredient in ingredients:
            cursor.execute(ingredient_dectect_query,
                            (ingredient, ))
            detection = cursor.fetchall()
            if not detection:
                self.conn.commit()
                return False
            codes.append(detection[0][0])

        cursor.execute(insert_recipe_query, (name, instrutions,
                                            servings, course, season))

        for code, amount in zip(codes, amounts):
            cursor.execute(insert_recipe_ingredient_query,
                            (code, name, amount))

        self.conn.commit()
        return True


