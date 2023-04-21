from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

GAME_ID_JSON_KEY = "gameId"

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({GAME_ID_JSON_KEY: game_id, "board": game.board})

@app.post("/api/score-word")
def score_word():
    """Takes a word and game id and lets us know if it's a valid word and on the board"""

    current_game = games[request.json.get(GAME_ID_JSON_KEY)]
    current_word = request.json.get("word")

    is_in_word_list = current_game.is_word_in_word_list(current_word)

    if not is_in_word_list:
        return jsonify({"result": "not-word"})

    is_on_board = current_game.check_word_on_board(current_word)

    if not is_on_board:
        return jsonify({"result": "not-on-board"})

    else:
        return jsonify({"result": "ok"})
