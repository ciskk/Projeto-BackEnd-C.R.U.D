
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

recipes = []
recipe_id_counter = 1

class Recipe(Resource):
    def get(self, recipe_id=None):
        if recipe_id:
            recipe = next((r for r in recipes if r['id'] == recipe_id), None)
            if recipe:
                return recipe, 200
            return {'message': 'Receita não encontrada'}, 404
        return recipes, 200

    def post(self):
        global recipe_id_counter
        data = request.get_json()

        name = data.get('nome')
        ingredients = data.get('ingredientes')
        preparation_method = data.get('modo_de_preparo')

        if not name or not ingredients or not preparation_method:
            return {'message': 'Nome, ingredientes e modo de preparo são obrigatórios'}, 400

        if not (2 <= len(name) <= 50):
            return {'message': 'O nome da receita deve ter entre 2 e 50 caracteres'}, 400

        if not (1 <= len(ingredients) <= 20):
            return {'message': 'A receita deve ter entre 1 e 20 ingredientes'}, 400

        if any(r['nome'].lower() == name.lower() for r in recipes):
            return {'message': 'Já existe uma receita com este nome'}, 400

        recipe = {
            'id': recipe_id_counter,
            'nome': name,
            'ingredientes': ingredients,
            'modo_de_preparo': preparation_method
        }
        recipes.append(recipe)
        recipe_id_counter += 1
        return recipe, 201

    def put(self, recipe_id):
        data = request.get_json()
        recipe = next((r for r in recipes if r['id'] == recipe_id), None)

        if not recipe:
            return {'message': 'Receita não encontrada'}, 404

        new_name = data.get('nome')
        new_ingredients = data.get('ingredientes')
        new_preparation_method = data.get('modo_de_preparo')

        if new_name is not None:
            if not (2 <= len(new_name) <= 50):
                return {'message': 'O nome da receita deve ter entre 2 e 50 caracteres'}, 400
            if new_name.strip() == '':
                return {'message': 'O nome da receita não pode ser vazio'}, 400
            if any(r['nome'].lower() == new_name.lower() and r['id'] != recipe_id for r in recipes):
                return {'message': 'Já existe outra receita com este nome'}, 400
            recipe['nome'] = new_name

        if new_ingredients is not None:
            if not (1 <= len(new_ingredients) <= 20):
                return {'message': 'A receita deve ter entre 1 e 20 ingredientes'}, 400
            recipe['ingredientes'] = new_ingredients

        if new_preparation_method is not None:
            recipe['modo_de_preparo'] = new_preparation_method

        return recipe, 200

    def delete(self, recipe_id):
        global recipes
        if not recipes:
            return {'message': 'A lista de receitas está vazia'}, 400

        recipe = next((r for r in recipes if r['id'] == recipe_id), None)
        if not recipe:
            return {'message': 'Receita não encontrada'}, 404

        recipes = [r for r in recipes if r['id'] != recipe_id]
        return {'message': 'Receita deletada', 'recipe': recipe}, 200

api.add_resource(Recipe, '/recipes', '/recipes/<int:recipe_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

