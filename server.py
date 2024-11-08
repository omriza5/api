from flask import Flask, Response,request
from flask_cors import CORS
from pokemon_utils import PokemonUtils
from pokemon_api import PokemonAPI
from db.pokemon_db import PokemonDB
from pokemon import Pokemon
import json

app = Flask(__name__)
CORS(app)

utils = PokemonUtils()
pokemonDB = PokemonDB()

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')
    
@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    pokemon_api = PokemonAPI()
    pokemons = pokemon_api.get_all_pokemons()
    rand_pokemom = utils.pick_random_pokemon(pokemons)
    
    pokemon_from_db = pokemonDB.get_pokemon_by_name(rand_pokemom)
    
    result = None
    if not pokemon_from_db:
        new_poke = pokemon_api.get_pokemon_details(rand_pokemom)
        new_poke = Pokemon.from_api(new_poke)
        pokemonDB.add_pokemon(str(new_poke.id),new_poke.name,new_poke.abilities,new_poke.image)
        result = new_poke.to_dict()
    else:
        result = pokemon_from_db[0]

    return Response(response=json.dumps(result),
                    status=200,
                    mimetype='application/json')
    
@app.route('/api/pokemons', methods=['GET'])
def get_all_pokemons():
    try:
        pokemons_from_db = pokemonDB.get_all_pokemons() 
        return Response(response=json.dumps(pokemons_from_db),
                        status=200,
                        mimetype='application/json')
    except Exception as e:
        return Response(response=json.dumps({"error": str(e)}),
                        status=500,
                        mimetype='application/json')
