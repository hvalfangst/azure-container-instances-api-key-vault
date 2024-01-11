import sys

from flask import jsonify, request
from config.module import AzureStorageAccountTablesConfig, AzureCredentials
from repository.module import HeroesRepository
from model.module import Hero

row_key_counter: int = 1
credential = AzureCredentials
azure_config = AzureStorageAccountTablesConfig("hvalfangststorageaccount", "hvalfangststoragetable", "Heroes")
heroes_repo = HeroesRepository(credential=credential.get_credential(azure_config.account_name), config=azure_config)


def create_hero_route():
    request_json = request.get_json()

    if not all(field in request_json for field in ['hero_name', 'hero_class', 'hero_damage']):
        error_message = "Fields hero_name, hero_class, and hero_damage are all required in the request JSON."
        return jsonify({"error": error_message}), 400

    try:
        hero_data = Hero(name=request_json['hero_name'],
                         hero_class=request_json['hero_class'],
                         hero_damage=request_json['hero_damage'])
        heroes_repo.create(row_key=row_key_counter, data=hero_data.to_dict())
        increment_row_key_counter()
        return jsonify({"message": "Successfully created hero."})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def list_heroes_route():
    try:
        heroes = heroes_repo.list()
        return jsonify({"heroes": [hero for hero in heroes]})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def get_hero_route(row_key: str):
    try:
        hero = heroes_repo.get(row_key=row_key)
        return jsonify({"hero": hero})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def delete_hero_route(row_key: str):
    try:
        heroes_repo.delete(row_key=row_key)
        return jsonify({"message": "Hero has been deleted"})
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return jsonify({"error": error_message})


def increment_row_key_counter():
    global row_key_counter
    row_key_counter += 1
