import threading
import asyncio
import random
from flask import Flask, request, jsonify, render_template
from pywizlight import wizlight, PilotBuilder
from pywizlight.exceptions import WizLightConnectionError
import requests

app = Flask(__name__)

home, away = (-1, -1)
TEAM_CODE = None
DATE = ""
COLOURS = []
BULBS = []
PLAYLIST_NAME = "OTR"

# BULB METHODS

async def turn_on_bulb(ip_address):
    try:
        bulb = wizlight(ip_address)
        await bulb.turn_on()
        print("Bulb, Turned on Successfully!")
    except Exception as e:
        print(f"Exception was thrown (Turn On): {e}")

async def turn_off_bulb(ip_address):
    try:
        bulb = wizlight(ip_address)
        await bulb.turn_off()
        print("Bulb, Turned off Successfully!")
    except Exception as e:
        print(f"Exception was thrown (Turn Off): {e}")

async def brightness_change(ip_address, brightness):
    try:
        bulb = wizlight(ip_address)
        await bulb.turn_on(PilotBuilder(brightness=brightness))
        print(f"Bulb Brightness changed to {brightness} Successfully!")
    except Exception as e:
        print(f"Exception was thrown (Brightness Changed): {e}")


async def colour_change(ip_address, colour):
    colour = tuple(colour)
    print(colour)
    try:
        bulb = wizlight(ip_address)
        if colour == (0, 0, 0):
            await bulb.turn_off()
        elif colour == (255, 255, 255):
            await bulb.turn_on(PilotBuilder(cold_white=255))
        else:
            await bulb.turn_on(PilotBuilder(rgb=colour))
        print(f"Bulb Brightness changed to {colour} Successfully!")
    except Exception as e:
        print(f"Exception was thrown (Colour Change): {e}")

async def goal(bulbs, colours):
    global PLAYLIST_NAME
    if TEAM_CODE == "TOR":
        PLAYLIST_NAME = "TOR"
    else:
        PLAYLIST_NAME = "OTR"
    
    colour_changes = 0

    while colour_changes < 15:
        for bulb in bulbs:
            await colour_change(bulb, random.choice(colours))
            if colour_changes % 2 == 0:
                await brightness_change(bulb, 100)
            else:
                await brightness_change(bulb, 100)
        colour_changes += 1
    for bulb in bulbs:
            await brightness_change(bulb, 50)

async def goal_other(bulbs, colours):
    global PLAYLIST_NAME
    if TEAM_CODE == "TOR":
        PLAYLIST_NAME = "TOR"
    else:
        PLAYLIST_NAME = "OTR"

    colour_changes = 0

    while colour_changes < 15:
        for bulb in bulbs:
            await colour_change(bulb, (255, 0, 0))
            if colour_changes % 2 == 0:
                await brightness_change(bulb, 100)
            else:
                await brightness_change(bulb, 100)
        colour_changes += 1
    for bulb in bulbs:
            await brightness_change(bulb, 50)


def get_game_score(api_url, team_abbrev, date):
    other = 0
    us = 0

    home_team_abrev = ""
    try:
        response = requests.get(api_url)
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
            
# Main Logic/Loop
async def background_task():
    global home, away
    home, away = (-1, 0)
    
    print("TEST")
    while True:
        if TEAM_CODE:
            print(TEAM_CODE)
        while TEAM_CODE:
            api_url = f"https://api-web.nhle.com/v1/scoreboard/{TEAM_CODE}/now/"
            response = requests.get(api_url)
            data = response.json()
            state = get_state(data)

            try:
                score = get_game_score(api_url, TEAM_CODE, DATE)
                if score[0] > home:
                    home, away = score
                    await goal(BULBS, COLOURS)
                elif score[1] > away:
                    home, away = score
                    await goal_other(BULBS, COLOURS)
                elif score[0] < home:
                    home, away = score
                elif score[1] < away:
                    home, away = score
                else:
                    home, away = score
                for bulb in BULBS:
                    await colour_change(bulb, random.choice(COLOURS))      
                    await brightness_change(bulb, 50)          
            except Exception as e:
                print(f"Exception was thrown: {e}")


def get_state(data):
    game_state = ""
    for games in data["gamesByDate"]:
        if games["date"] == DATE:
            for ids in games["games"]:
                game_state = ids["gameState"]
    return game_state


def run_background_task():
    asyncio.run(background_task())

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
    thread = threading.Thread(target=run_background_task, daemon=True)
    thread.start()
    app.run(port = 80, host = '0.0.0.0', debug = False)