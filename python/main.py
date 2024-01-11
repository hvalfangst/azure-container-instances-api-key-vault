from flask import Flask
from route.module import create_hero_route, list_heroes_route, get_hero_route, delete_hero_route

flask_api = Flask(__name__)

# Register routes
flask_api.add_url_rule("/heroes", methods=["POST"], view_func=create_hero_route)
flask_api.add_url_rule("/heroes", methods=["GET"], view_func=list_heroes_route)
flask_api.add_url_rule("/heroes/<row_key>", methods=["GET"], view_func=get_hero_route)
flask_api.add_url_rule("/heroes/<row_key>", methods=["DELETE"], view_func=delete_hero_route)

# Azure Container Instances targets port 80
if __name__ == "__main__":
    flask_api.run(debug=False, host="0.0.0.0", port=80)
