from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

home, away = (-1, -1)
TEAM_CODE = None
DATE = ""
COLOURS = []
BULBS = []

@app.route("/", methods=['POST'])
def index():
    # Global Variables Passed Through Webserver
    global TEAM_CODE
    global DATE
    global COLOURS
    global BULBS

    data = request.get_json()

    TEAM_CODE = data["team"]
    DATE = data["team"]
    BULBS = data["bulbs"]
    COLOURS = data["colours"]

    response = {
        "status": "success",
        "message": "Team Abrv., Game Date, Bulbs, and Colours Set! GO! {TEAM_CODE}! GO!",
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port = 80, host = '0.0.0.0', debug = False)