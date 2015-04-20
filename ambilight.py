#!/usr/bin/python

from phue import Bridge
import math
import json
import requests
import colorsys
from time import sleep
import logging

bridge_ip = '192.168.178.47'
television_ip = '192.168.178.79'

# Enter the ip of your bridge here
b = Bridge(bridge_ip)
logging.basicConfig()
# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
b.get_api()

lights = b.lights

# Print light names
for l in lights:
    print(l.name)

light_names = b.get_light_objects('name')

television_pulling_url = 'http://' + television_ip + ':1925/1/ambilight/processed'

def change_color_light(color, light):
	h, l, s = colorsys.rgb_to_hls(color['r'] / 255.0, color['g'] / 255.0, color['b'] / 255.0)
	command = {'transitiontime' : 3, 'hue' : int(math.floor(h * 65536.0)), 'sat' : int(s * 255.0), 'bri' : int(l * 255)}
	b.set_light(light, command)

while True:	
	response = requests.get(url=television_pulling_url)
	response_data = json.loads(response.text)
	change_color_light(response_data['layer1']['left']['1'], 'Sofalamp oben')
	change_color_light(response_data['layer1']['left']['1'], 'Leinwand oben links')
	change_color_light(response_data['layer1']['left']['0'], 'Sofalamp unten')
	change_color_light(response_data['layer1']['right']['1'], 'Leinwand oben rechts')
	sleep(0.3)
