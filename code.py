import time
from UnicornHATMini import UnicornHATMini

import wifi, socketpool, ssl
import adafruit_requests
import json

try:
    from secrets import secrets
except ImportError:
    print("Wifi secrets are kept in secrets.py")
    raise

# replace the uppercase letters with your keylight air id
keylight1 = "http://elgato-key-light-air-YOUR-KEY-LIGHT-AIR-ID.local:9123/elgato/lights"
keylight2 = "http://elgato-key-light-air-YOUR-KEY-LIGHT-AIR-ID.local:9123/elgato/lights"

unicornhatmini = UnicornHATMini()

# Connect to WiFi
print("Connecting to wifi")
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
print("my IP address:", wifi.radio.ipv4_address)

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
headers = {'Content-type': 'application/json'}

def toggleLight(light_url, state):
    payload = {
        "numberOfLights":1,
        "lights":[{
            "on": state,
            "brightness":30,
            "temperature":153
        }]
    }

    try:
        response = requests.put(light_url, data=json.dumps(payload), headers=headers)
        print(response.status_code)

        if response.status_code == 200:
            print(response.json())
            time.sleep(1)
    except Exception as e:
        print(e)


while True:
    buttonA = unicornhatmini.getButtonAState()
    buttonB = unicornhatmini.getButtonBState()

    if not buttonA:
        print("Pressing button A")
        toggleLight(keylight1, 0)
        time.sleep(0.25)

    if not buttonB:
        print("Pressing button B")
        toggleLight(keylight2, 1)
        time.sleep(0.25)
