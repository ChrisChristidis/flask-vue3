from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)

app.config.from_object(__name__)

# Comma-separated list of allowed origins. Defaults to "*" for local/dev so
# Docker-compose works out of the box. Set CORS_ORIGINS to your real frontend
# URL in production (e.g. https://flask-vue3-frontend.onrender.com).
_origins_raw = os.getenv("CORS_ORIGINS", "*")
_origins = [o.strip() for o in _origins_raw.split(",")] if _origins_raw != "*" else "*"
CORS(app, resources={r"/*": {"origins": _origins}})

GAMES = [
    {"id": uuid.uuid4().hex, "title": "2k24", "genre": "sports", "played": True},
    {
        "id": uuid.uuid4().hex,
        "title": "Evil Within",
        "genre": "horror",
        "played": False,
    },
    {
        "id": uuid.uuid4().hex,
        "title": "The last of us",
        "genre": "survive",
        "played": True,
    },
    {
        "id": uuid.uuid4().hex,
        "title": "Days gone",
        "genre": "horror/survival",
        "played": False,
    },
    {"id": uuid.uuid4().hex, "title": "mario", "genre": "retro", "played": True},
]


# GET and POST route handler
@app.route("/games", methods=["GET", "POST"])
def all_games():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        GAMES.append(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "genre": post_data.get("genre"),
                "played": post_data.get("played"),
            }
        )
        response_object["message"] = "Game Added!"

    if request.method == "GET":
        response_object["games"] = GAMES

    return jsonify(response_object)


# PUT and DELETE route handler
@app.route("/games/<game_id>", methods=["PUT", "DELETE"])
def single_games(game_id):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_game(game_id)

        GAMES.append(
            {
                "uuid": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "genre": post_data.get("genre"),
                "played": post_data.get("played"),
            }
        )
        response_object["message"] = "Game Updated!"

    if request.method == "DELETE":
        remove_game(game_id)
        response_object["message"] = "Game Removed!"

    return jsonify(response_object)


# Remove game
def remove_game(game_id):
    for game in GAMES:
        if game["id"] == game_id:
            GAMES.remove(game)
            return True

    return False


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
