from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

home, away = (-1, -1)
TEAM_CODE = None
DATE = ""
COLOURS = []
BULBS = []

def get_game_score(api_url, team_abbrev, date):
    other = 0
    us = 0

    home_team_abrev = ""
    try:
        response = request.get(api_url)
        data = response.json()
        for game in data["gamesByDate"]:
            if game["date"] == DATE:
                for id in game["games"]:
                    home_team_goals = id["homeTeam"]["score"]
                    away_team_goals = id["homeTeam"]["score"]
                    if home_team_goals != None:
                        us = home_team_goals
                    if away_team_goals != None:
                        other = away_team_goals
                    home_team_abrev    
        if home_team_abrev != home_team_abrev:
            return (other, us)    
        else:
            return (us, other)
    except Exception as e:
        print(f"An Error has Occured: {e}")
            


@app.route("/", methods=['POST'])
def index():
    # Global Variables Passed Through Webserver
    global TEAM_CODE
    global DATE
    global COLOURS
    global BULBS

    data = request.get_json()

    TEAM_CODE = data["team"]
    DATE = data["date"].split("T")[0]
    BULBS = data["bulbs"]
    COLOURS = data["colours"]

    response = {
        "status": "success",
        "message": f"Team Abrv., Game Date, Bulbs, and Colours Set! GO! {TEAM_CODE}! GO!",
    }

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port = 80, host = '0.0.0.0', debug = False)