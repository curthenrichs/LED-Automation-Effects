'''
x0   tornado
x1	tropical storm
x2	hurricane
x3	severe thunderstorms
x4	thunderstorms
x5	mixed rain and snow
x6	mixed rain and sleet
x7	mixed snow and sleet
x8	freezing drizzle
x9	drizzle
x10	freezing rain
x11	showers
x12	showers
x13	snow flurries
x14	light snow showers
x15	blowing snow
x16	snow
x17	hail
x18	sleet
x19	dust
x20	foggy
x21	haze
x22	smoky
x23	blustery
x24	windy
x25	cold
x26	cloudy
x27	mostly cloudy (night)
x28	mostly cloudy (day)
x29	partly cloudy (night)
x30	partly cloudy (day)
x31	clear (night)
x32	sunny
x33	fair (night)
x34	fair (day)
x35	mixed rain and hail
x36	hot
x37	isolated thunderstorms
x38	scattered thunderstorms
x39	scattered thunderstorms
x40	scattered showers
x41	heavy snow
x42	scattered snow showers
x43	heavy snow
x44	partly cloudy
x45	thundershowers
46	snow showers
x47	isolated thundershowers
x3200	not available
'''

import color_wheel
import led_server_api
import yahoo_api
import effects
import json
import random
import time
random.seed()


def _severe_weather_effect(rgb, iteration, cycleMax):
    pass


def _storming_weather_effect(rgb, level, iteration, cycleMax):
    pass


def _raining_weather_effect(rgb, level, iteration, cycleMax):
    pass


def _snowing_weather_effect(rgb, level, iteration, cycleMax):
    pass


def _wind_weather_effect(rgb, level, iteration, cycleMax):
    pass


def _map_temperature_to_angle(temp, t_range=(0, 100), a_range=(0, 360)):
    if temp < t_range[0]:
        temp = t_range[0]
    elif temp > t_range[1]:
        temp = t_range[1]
    return ((a_range[1] - a_range[0]) / (t_range[1] - t_range[0])) * (temp - t_range[0])


def _weather_condition_effects(rgb, condition, iteration, cycleMax):
    c = condition.lower()
    if c == 'tornado' or c == 'tropical storm' or c == 'hurricane' or c == 'severe thunderstorms':
        rgb = _severe_weather_effect(rgb, iteration, cycleMax)
    elif c == 'thunderstorms' or c == 'isolated thunderstorms' or c == 'scattered thunderstorms' or c == 'thundershowers' or c == 'isolated thundershowers':
        rgb = _storming_weather_effect(rgb, 1, iteration, cycleMax)
    elif c == 'mixed rain and snow' or c == 'mixed rain and sleet' or c == 'mixed snow and sleet' or c == 'sleet':
        rgb = _raining_weather_effect(_snowing_weather_effect(rgb, 1, iteration, cycleMax), 1, iteration, cycleMax)
    elif c == 'freezing drizzle' or c == 'drizzle' or c == 'scattered showers':
        rgb = _raining_weather_effect(rgb, 0, iteration, cycleMax)
    elif c == 'freezing rain' or c == 'showers':
        rgb = _raining_weather_effect(rgb, 1, iteration, cycleMax)
    elif c == 'snow flurries' or c == 'light snow showers':
        rgb = _snowing_weather_effect(rgb, 0, iteration, cycleMax)
    elif c == 'blowing snow':
        rgb = _wind_weather_effect(_snowing_weather_effect(rgb, 1, iteration, cycleMax), 1, iteration, cycleMax)
    elif c == 'snow' or c == 'heavy snow' or c == 'scattered snow showers' or c == 'snow showers':
        rgb = _snowing_weather_effect(rgb, 1, iteration, cycleMax)
    elif c == 'hail' or c == 'mixed rain and hail':
        rgb = _storming_weather_effect(_snowing_weather_effect(rgb, 1, iteration, cycleMax), 1, iteration, cycleMax)
    elif c == 'blustery' or c == 'windy':
        rgb = _wind_weather_effect(rgb, 1, iteration, cycleMax)
    return rgb


def outside_temperature_scale(woeid, normalize=(1, 1, 1), brightness=effects.default_brightness_ftn):
    msg = yahoo_api.get_weather(woeid)
    temp = float(msg["query"]["results"]["channel"]["item"]["condition"]["temp"])
    condition = msg["query"]["results"]["channel"]["item"]["condition"]["text"]

    angle = 240 - _map_temperature_to_angle(temp, (0, 90), (0, 240))
    base_rgb = color_wheel.get(angle, True, 'sine', normalize)
    base_rgb = tuple(brightness(angle) * x for x in base_rgb)

    return base_rgb, condition


if __name__ == "__main__":
    woeid = yahoo_api.get_woeid('milwaukee', 'wi')

    while True:
        base_rgb, condition = outside_temperature_scale(woeid)

        for i in color_wheel.frange(0, 360, 0.05):
            rgb = _weather_condition_effects(base_rgb, condition, i, 360)
            led_server_api.set(rgb)
            time.sleep(0.05)
