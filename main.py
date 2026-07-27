from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from pokedex import POKEDEX
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("geheime_code")
lijst_pokemon = POKEDEX


@app.route("/")
def index ():
    return render_template(
        "index.html"
    )
# lijst alle pokemons

@app.route("/api/pokemon", methods=["GET"])
def get_pokemon ():
    return jsonify(lijst_pokemon)

#een pokemon

@app.route("/api/pokemon/<int:pokemon_id>", methods=["GET"])
def get_one_pokemon (pokemon_id):

    pokemon = vind_juiste_pokemon(pokemon_id)

    if pokemon :
        return jsonify(pokemon)
    else:
        return jsonify({"error": f"Geen pokemon met id {pokemon_id} gevonden"}), 404

def vind_juiste_pokemon (pokemon_id):
    for pokemon in lijst_pokemon:
        if pokemon["id"] == pokemon_id:
            return pokemon
    return None

# een pokemon eigenschap vinden

@app.route ("/api/pokemon/search", methods=["GET"])
def search_pokemon ():
    zoek = request.args

    name = zoek.get("name")
    type = zoek.get("type")

    juiste_pokemon = lijst_pokemon

    if not (name or type):
        return jsonify({"error":"Er werd geen name of type geselecteerd"}), 400

    if name:
        juiste_pokemon = [m for m in juiste_pokemon if m["name"] == name]

    if type:
        juiste_pokemon = [m for m in juiste_pokemon if type in m["type"]]

    if not juiste_pokemon:
        return jsonify({"error": "Er werd geen pokemon gevonden die aan deze creteria vodoed!"}), 404

    return jsonify(juiste_pokemon)

# een pokemon toevoegen

@app.route ("/api/pokemon", methods=["POST"])
def pokemon_toevoegen ():

    nieuwe_pokemon = request.get_json()

    if "name" not in nieuwe_pokemon:
        return jsonify({
            "error":"Er moet een naam mee gegeven worden om een nieuwe pokemon te kunnen aanmaken!"
        }),400
    for pokemon in POKEDEX:
        if pokemon["name"] == nieuwe_pokemon["name"]:
            return jsonify({
                "error":f"De pokemon met naam '{pokemon['name']}' bestaat al."
            }), 409

    nieuwe_pokemon["id"] = len(POKEDEX) + 1
    POKEDEX.append(nieuwe_pokemon)

    return jsonify(nieuwe_pokemon),201

# een pokemon bijwerken

@app.route("/api/pokemon/<int:pokemon_id>", methods=["PUT"])
def wijzig_pokemon (pokemon_id):
    pokemon = next (
        (m for m in POKEDEX if m["id"] == pokemon_id), None )
    if not pokemon:
        return jsonify({"error":"Pokemon not found"}),404

    gewijzigde_pokemon = request.get_json()
    pokemon.update(gewijzigde_pokemon)
    return jsonify(pokemon),200

# een pokemon verwijderen

@app.route("/api/pokemon/<int:pokemon_id>", methods=["DELETE"])
def verwijder_pokemon (pokemon_id):
    te_verwijderen_pokemon = next (
        (m for m in POKEDEX if m["id"] == pokemon_id), None )
    if not te_verwijderen_pokemon :
       return jsonify({"error":f"Pokemon met '{pokemon_id}' werd niet gevonden"}), 404

    POKEDEX.remove(te_verwijderen_pokemon)
    return jsonify({"message":"Pokemon werd correct verwijderd!"})


if __name__ == "__main__":
    app.run(debug=True)