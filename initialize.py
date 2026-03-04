import requests
import re
import time
from datetime import datetime

current_time = datetime.now()
time_coded = current_time.strftime("%Y-%m-%dT%H:%M:%S")

pattern = r"^http:\/\/\d{1,3}(\.\d{1,3}){3}\/$"
not_work = True

while not_work:
    url = "http://" + input("What is the IP address of the flask server(i.e. 127.0.0.0): ") + "/"

    if re.search(pattern, url):
        not_work = False

bulbs_amount = int(input("How many Wiz Bulbs do you have: "))
bulbs = []
for i in range(bulbs_amount):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    not_work = True
    bulb = ""
    while not_work:
        bulb = input(f"What is the IP address of bulb #{i + 1} (i.e. 127.0.0.0): ") 
        if re.search(pattern, bulb):
            not_work = False
    bulbs.append(bulb)

colours_amount = int(input("How many Colours do you want: "))
colours = []

for i in range(colours_amount):
    r = int(input(f"What is the R value of colour {i + 1}: "))
    g = int(input(f"What is the G value of colour {i + 1}: "))
    b = int(input(f"What is the B value of colour {i + 1}: "))
    colours.append((r, g, b))

payload = {"team": input("What is the 3 digit team code (i.e. TOR): "), "date": time_coded, "bulbs": bulbs, "colours": colours}

print(payload)

try:
    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

except requests.exceptions.RequestException as e:
    print("Error sending POST request:", e)