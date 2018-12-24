import requests
import json

CLIENT_ID = 'Fill this in'
CLIENT_SECRET = 'Fill this in'

WEATHER_API_YAHOO = 'https://query.yahooapis.com/v1/public/yql'

def get_woeid(city, state):
    woeid_query = {'q' : 'select woeid from geo.places where text=' + '"' + city +', ' + state + '"', 'format' : 'json'}
    woeid_result = requests.get(WEATHER_API_YAHOO, params = woeid_query)
    woeid_json = json.loads(woeid_result.text)
    return woeid_json["query"]["results"]["place"]["woeid"]

def get_weather(woeid):
    weather_query = {'q' : 'select * from weather.forecast where woeid=' + woeid, 'format' : 'json'}
    weather_result = requests.get(WEATHER_API_YAHOO, params = weather_query)
    weather_json = json.loads(weather_result.text)
    return weather_json
