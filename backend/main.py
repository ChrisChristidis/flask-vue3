"""
Games Library API.

Runtime mode:
  - If MONGODB_URL is set, persist to MongoDB (collection: games).
  - Otherwise, use an in-memory list seeded with sample games (resets every
    restart; fine for the free Render demo).

Configuration:
  - MONGODB_URL  : Atlas URL or mongodb://user:pass@host:27017/
  - CORS_ORIGINS : comma-separated origin list, or "*" (default).
  - PORT         : port to bind (default 5000); Render injects its own.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
app.config.from_object(__name__)

# -------- CORS --------
_origins_raw = os.getenv("CORS_ORIGINS", "*")
_origins = (
    [o.strip() for o in _origins_raw.split(",")] if _origins_raw != "*" else "*"
)
CORS(app, resources={r"/*": {"origins": _origins}})

# -------- Storage backend --------
MONGODB_URL = os.getenv("MONGODB_URL")
USE_MONGO = bool(MONGODB_URL)
games_collection = None

if USE_MONGO:
    from pymongo import MongoClient

    client = MongoClient(MONGODB_URL)
    db = client.flask_database
    games_collection = db.games
    app.logger.info("Using MongoDB persistence")
else:
    app.logger.info("Using in-memory storage (set MONGODB_URL to persist)")

# Seed data for the in-memory mode
GAMES = [
    {
        "id": uuid.uuid4().hex,
        "title": "2k24",
        "genre": "sports",
        "played": True,
        "cover_url": "",
    },
    {
        "id": uuid.uuid4().hex,
        "title": "Evil Within",
        "genre": "horror",
        "played": False,
        "cover_url": "",
    },
    {
        "id": uuid.uuid4().hex,
        "title": "The last of us",
        "genre": "survive",
        "played": True,
        "cover_url": "",
    },
    {
        "id": uuid.uuid4().hex,
        "title": "Days gone",
        "genre": "horror/survival",
        "played": False,
        "cover_url": "",
    },
    {
        "id": uuid.uuid4().hex,
        "title": "mario",
        "genre": "retro",
        "played": True,
        "cover_url": "",
    },
]


def _serialize(post_data):
    """Build a game dict from request JSON."""
    return {
        "id": uuid.uuid4().hex,
        "title": post_data.get("title", ""),
        "genre": post_data.get("genre", ""),
        "played": bool(post_data.get("played", False)),
        "cover_url": post_data.get("cover_url", ""),
    }


def _list_games():
    if USE_MONGO:
        return list(games_collection.find({}, {"_id": 0}))
    return GAMES


def _add_game(game):
    if USE_MONGO:
        games_collection.insert_one(game)
    else:
        GAMES.append(game)


def _remove_game(game_id):
    if USE_MONGO:
        result = games_collection.delete_one({"id": game_id})
        return result.deleted_count > 0
    for game in GAMES:
        if game["id"] == game_id:
            GAMES.remove(game)
            return True
    return False


# -------- Routes --------
@app.route("/games", methods=["GET", "POST"])
def all_games():
    response_object = {"status": "success"}
    if request.method == "POST":
        post_data = request.get_json() or {}
        _add_game(_serialize(post_data))
        response_object["message"] = "Game Added!"

    if request.method == "GET":
        response_object["games"] = _list_games()

    return jsonify(response_object)


@app.route("/games/<game_id>", methods=["PUT", "DELETE"])
def single_game(game_id):
    response_object = {"status": "success"}

    if request.method == "PUT":
        post_data = request.get_json() or {}
        _remove_game(game_id)
        new_game = _serialize(post_data)
        # Preserve the id when updating so the UI's key doesn't churn.
        new_game["id"] = game_id
        _add_game(new_game)
        response_object["message"] = "Game Updated!"

    if request.method == "DELETE":
        _remove_game(game_id)
        response_object["message"] = "Game Removed!"

    response_object["games"] = _list_games()
    return jsonify(response_object)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "storage": "mongo" if USE_MONGO else "memory"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
