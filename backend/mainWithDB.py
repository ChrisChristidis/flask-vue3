from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import uuid
import os

app = Flask(__name__)

# Get MongoDB URL from environment variable
mongodb_url = os.getenv("MONGODB_URL")

client = MongoClient(mongodb_url)

# This a mongodb database
db = client.flask_database

# This a games collection
games_collection = db.games

app.config.from_object(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


# GET and POST route handler
@app.route("/games", methods=["GET", "POST"])
def all_games():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json()
        games_collection.insert_one(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "genre": post_data.get("genre"),
                "played": post_data.get("played"),
            }
        )

        response_object["message"] = "Game Added!"

    if request.method == "GET":
        response_object["games"] = get_all_games()

    return jsonify(response_object)


# PUT and DELETE route handler
@app.route("/games/<game_id>", methods=["PUT", "DELETE"])
def single_games(game_id):
    response_object = {"status": "success"}
    if request.method == "PUT":
        post_data = request.get_json()
        remove_game(game_id)

        games_collection.insert_one(
            {
                "id": uuid.uuid4().hex,
                "title": post_data.get("title"),
                "genre": post_data.get("genre"),
                "played": post_data.get("played"),
            }
        )
        response_object["message"] = "Game Updated!"

    if request.method == "DELETE":
        remove_game(game_id)
        response_object["message"] = "Game Removed!"

    response_object["games"] = get_all_games()
    return jsonify(response_object)


# Get all games
def get_all_games():
    return list(games_collection.find({}, {"_id": 0}))


# Remove game
def remove_game(game_id):
    for game in get_all_games():
        if game["id"] == game_id:
            games_collection.delete_one({"id": game_id})
            return True

    return False


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
