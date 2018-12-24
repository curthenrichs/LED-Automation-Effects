import time
import requests

LED_SERVICE_ADDRESS = '192.168.1.57:5000'
LED_SERVICE_SET = '/lights/set'
LED_SERVICE_OFF = '/lights/off'
LED_SERVICE_ROUTES = '/routes'
LED_SERIVCE_INDEX = '/'

def set(rgb):
    rgb = tuple((254.85 / 255) * x + 0.15 for x in rgb)
    r = requests.get('http://' + LED_SERVICE_ADDRESS + LED_SERVICE_SET, params = {'r' : rgb[0], 'g' : rgb[1], 'b' : rgb[2]})
    return r

def off():
    r = requests.get('http://' + LED_SERVICE_ADDRESS + LED_SERVICE_OFF)
    return r

def routes():
    r = requests.get('http://' + LED_SERVICE_ADDRESS + LED_SERVICE_ROUTES)
    return r

def index():
    r = requests.get('http://' + LED_SERVICE_ADDRESS + LED_SERIVCE_INDEX)
    return r

if __name__ == "__main__":
    off()
