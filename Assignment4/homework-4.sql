/*
You need to add checks, constraints, or triggers to add the following functionality to the database:

- When an order is inserted into the order table, the database should check the following:
  - whether the ingredients needed for the recipe are present in sufficient quantity in the inventory table.
    If not, the order should be rejected.
  - whether or not the recipe specified in the order conforms to the `kosher` requirement.
    If an order is kosher (`kosher=TRUE`), the recipe must not contain any non-kosher ingredients.
    If the order is not kosher, there is no requirement.
  - whether the order starts with a value in the `filled` column.
    An order should not be permitted to start with a value for the `filled` column.
- When the order table is updated so that a timestamp is added to the
    `filled` column of a tuple (denoting when the order was filled), the ingredients should be subtracted from inventory.
- Once a timestamp has been added to the 'filled' column, it shouldn't be able to be changed.
*/

-- Put your SQL here

-- 1
CREATE FUNCTION get_inventory_check()
RETURNS trigger
AS $$
    BEGIN
        IF EXISTS(
            SELECT *
            FROM(
                recipe_ingredient
            JOIN
                inventory
            ON recipe_ingredient.ingredient = inventory.ing_id)
            WHERE ((inventory.amount / recipe_ingredient.amount) < NEW.quantity)
            AND recipe_ingredient.recipe = NEW.recipe) THEN
            RETURN NULL;
        END IF;

    -- kosher check
        IF (NEW.kosher = TRUE) AND
        EXISTS(
            SELECT *
            FROM(
                recipe_ingredient
            JOIN
                ingredient
            ON recipe_ingredient.ingredient = ingredient.id)
            WHERE recipe_ingredient.recipe = NEW.recipe
            AND ingredient.is_kosher = FALSE
        ) THEN
            RETURN NULL;
        END IF;

    -- filled null test
        IF NEW.filled IS NOT NULL THEN
            RETURN NULL;
        END IF;

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER inventory_check
    BEFORE INSERT on orders
    FOR EACH ROW
    EXECUTE PROCEDURE get_inventory_check();


CREATE FUNCTION get_update_inventory()
RETURNS trigger
AS
$$
    BEGIN
        IF OLD.filled IS NOT NULL THEN
            RETURN NULL;
        END IF;
    -- update table
        UPDATE
            inventory
        SET
            amount = new_inventory.amount
        FROM(
            SELECT ing_id,
                    (inventory.amount - NEW.quantity * recipe_ingredient.amount) AS amount
            FROM(
                recipe_ingredient
            JOIN
                inventory
            ON recipe_ingredient.ingredient = inventory.ing_id)
            WHERE recipe_ingredient.recipe = NEW.recipe) new_inventory
        WHERE new_inventory.ing_id = inventory.ing_id;
        RETURN  NEW;
    END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_inventory
    BEFORE UPDATE on orders
    FOR EACH ROW
    EXECUTE PROCEDURE get_update_inventory();
