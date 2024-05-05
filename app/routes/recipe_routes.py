from flask import Blueprint, request, jsonify
from ..models.recipe import Recipe, db

recipe_blueprint = Blueprint('recipes', __name__)

@recipe_blueprint.route('/recipes', methods=['POST'])
def create_recipe():
    try:
        data = request.json
        recipe = Recipe(
            title=data['title'],
            making_time=data['making_time'],
            serves=data['serves'],
            ingredients=data['ingredients'],
            cost=data['cost']
        )
        db.session.add(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe successfully created!", "recipe": [recipe.serialize]}), 200
    except KeyError as e:
        return jsonify({"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}), 400

@recipe_blueprint.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify({"recipes": [recipe.serialize for recipe in recipes]}), 200

@recipe_blueprint.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        return jsonify({"message": "Recipe details by id", "recipe": [recipe.serialize]}), 200
    else:
        return jsonify({"message": "No recipe found"}), 404

@recipe_blueprint.route('/recipes/<int:recipe_id>', methods=['PATCH'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        data = request.json
        recipe.title = data.get('title', recipe.title)
        recipe.making_time = data.get('making_time', recipe.making_time)
        recipe.serves = data.get('serves', recipe.serves)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        recipe.cost = data.get('cost', recipe.cost)
        db.session.commit()
        return jsonify({"message": "Recipe successfully updated!", "recipe": [recipe.serialize]}), 200
    else:
        return jsonify({"message": "No recipe found"}), 404

@recipe_blueprint.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe successfully removed!"}), 200
    else:
        return jsonify({"message": "No recipe found"}), 404

