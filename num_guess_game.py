from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ add this
import random, math

app = Flask(__name__)
CORS(app)  # ✅ allow frontend from port 5500 to talk to backend

games = {}

def max_tries_for_range(max_value):
    return max(3, math.ceil(math.log2(max_value)) * 1)

@app.route("/start", methods=["POST"])
def start_game():
    data = request.json
    difficulty = data.get("difficulty", "easy").lower()

    if difficulty == "easy":
        low, high = 1, 20
    elif difficulty == "medium":
        low, high = 1, 100
    else:
        low, high = 1, 1000

    secret = random.randint(low, high)
    max_tries = max_tries_for_range(high - low + 1)
    game_id = "session_1"

    games[game_id] = {
        "low": low,
        "high": high,
        "secret": secret,
        "tries": 0,
        "max_tries": max_tries,
        "score": 0
    }

    return jsonify({
        "game_id": game_id,
        "low": low,
        "high": high,
        "max_tries": max_tries
    })

@app.route("/guess", methods=["POST"])
def make_guess():
    data = request.json
    game_id = data.get("game_id")
    guess = int(data.get("guess"))

    game = games.get(game_id)
    if not game:
        return jsonify({"error": "No active game"}), 400

    game["tries"] += 1
    low, high, secret = game["low"], game["high"], game["secret"]
    max_tries, tries = game["max_tries"], game["tries"]

    if guess == secret:
        score = max(0, (max_tries - tries + 1)) * 10
        game["score"] = score
        return jsonify({"result": "win", "score": score, "tries": tries})

    remaining = max_tries - tries
    hint = "higher" if guess < secret else "lower"
    diff = abs(secret - guess)
    if diff <= max(1, (high - low) // 20):
        closeness = "very close"
    elif diff <= max(2, (high - low) // 10):
        closeness = "close"
    else:
        closeness = "far"

    if remaining <= 0:
        return jsonify({"result": "lose", "secret": secret})

    return jsonify({
        "result": "continue",
        "hint": hint,
        "closeness": closeness,
        "remaining": remaining
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
