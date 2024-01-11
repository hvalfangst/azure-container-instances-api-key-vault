import sys
from flask import Flask, jsonify, request
from config.module import get_credential
from repository.module import init_heroes_table, create_hero, get_hero, list_heroes, delete_hero, to_dict

app = Flask(__name__)
credential = get_credential()
row_key_counter: int = 1


@app.route("/heroes", methods=["POST"])
def create_hero_route():
    """
    Endpoint to create a new entity.

    JSON Payload:
    {
        "hero_name": "Hero Name",
        "hero_class": "Hero Class",
        "hero_damage": 100
    }
    """
    request_json = request.get_json()

    # Validate required fields in the request JSON
    if 'hero_name' not in request_json or 'hero_class' not in request_json or 'hero_damage' not in request_json:
        error_message = "Fields hero_name, hero_class, and hero_damage are all required in the request JSON."
        return jsonify({"error": error_message}), 400

    try:
        heroes_table = init_heroes_table(credential=credential)
        create_hero(table=heroes_table, row_key=row_key_counter, data=to_dict(request_json))
        increment_row_key_counter()
        return jsonify({"message": f"Successfully created hero."})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


@app.route("/heroes", methods=["GET"])
def list_heroes_rote():
    """
    Endpoint to retrieve all entities with partition key 'Heroes'.
    """
    try:
        heroes_table = init_heroes_table(credential=credential)
        heroes = list_heroes(heroes_table)
        return jsonify({"heroes": list(heroes)})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


@app.route("/heroes/<row_key>", methods=["GET"])
def get_hero_route(row_key: str):
    """
    Endpoint to retrieve an entity by row key.
    """
    try:
        heroes_table = init_heroes_table(credential=credential)
        hero = get_hero(table=heroes_table, row_key=row_key)
        return jsonify({"hero": hero})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


@app.route("/heroes/<row_key>", methods=["DELETE"])
def delete_hero_route(row_key: str):
    try:
        heroes_table = init_heroes_table(credential=credential)
        delete_hero(table=heroes_table, row_key=row_key)
        return jsonify({"message": "Hero has been deleted"})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def increment_row_key_counter():
    """
    Increment the global row key counter.
    """
    global row_key_counter
    row_key_counter += 1


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
