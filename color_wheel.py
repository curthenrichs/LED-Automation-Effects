import math
import time
import led_server_api

PEAK_RED_ANGLE = 0
PEAK_GREEN_ANGLE = (2 / 3) * math.pi
PEAK_BLUE_ANGLE = (4 / 3) * math.pi
COLOR_PERIOD = 2 * math.pi

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def _red_ramp(theta):
    retval = 0;
    if theta <= math.pi:
        retval = 1 - (theta % math.pi) / math.pi
    elif theta >= 2 * math.pi:
        retval = (theta % math.pi) / math.pi
    return retval

def _green_ramp(theta):
    retval = 0;
    if theta >= 0 and theta <= 2 * math.pi:
        retval = 1 - abs((theta % (2 * math.pi)) / math.pi - 1)
    return retval

def _blue_ramp(theta):
    retval = 0;
    if theta >= math.pi and theta <= 3 * math.pi:
        retval = 1 - abs(((theta - math.pi) % (2 * math.pi)) / math.pi - 1)
    return retval

def _red_sine(theta):
    retval = 0;
    if theta <= math.pi:
        retval = 0.5 * math.sin(theta + (1 / 2) * math.pi) + 0.5
    elif theta >= 2 * math.pi:
        retval = 0.5 * math.sin(theta + (3 / 2) * math.pi) + 0.5
    return retval

def _green_sine(theta):
    retval = 0;
    if theta >= 0 and theta <= 2 * math.pi:
        retval = 0.5 * math.sin(theta + (3 / 2) * math.pi) + 0.5
    return retval

def _blue_sine(theta):
    retval = 0;
    if theta >= math.pi and theta <= 3 * math.pi:
        retval = 0.5 * math.sin(theta - (3 / 2) * math.pi) + 0.5
    return retval

def get(theta, degrees=False, form="ramp", normalize=(1,1,1)):
    '''
    Return color as RGB tuple given the movement around the color wheel for
    Theta which is noramally in radians until specified as degrees
    '''
    if degrees:
        theta = theta / 180 * math.pi
    theta = theta % (2 * math.pi)
    theta = (3 / 2) * theta

    rgb = (0,0,0)
    if form == "ramp":
        rgb = (_red_ramp(theta),_green_ramp(theta),_blue_ramp(theta))
    elif form == "sine":
        rgb = (_red_sine(theta),_green_sine(theta),_blue_sine(theta))
    return (rgb[0] * normalize[0],rgb[1] * normalize[1],rgb[2] * normalize[2])
