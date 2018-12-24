import color_wheel
import led_server_api
import time
import math

def default_brightness_ftn(theta):
    return 255

def _rainbow_adjusted_brightness_ftn(theta, degrees=False):
    retval = 0

    if degrees:
        theta = theta / 180 * math.pi
    theta = theta % (2 * math.pi)
    theta = (3 / 2) * theta

    if theta >= 0 and theta < math.pi / 2:
        retval = 0.35 * math.cos(2 * theta) + 0.6
    elif theta >= math.pi / 2 and theta < math.pi * 3 / 2:
        retval = 0.25
    elif theta >= math.pi * 3 / 2 and theta < math.pi * 2:
        retval = 0.125 * math.cos(2 * theta - math.pi / 2) + 0.375
    elif theta >= math.pi * 2 and theta < math.pi * 5 / 2:
        retval = 0.5 * math.cos(2 * theta) + 0.45
    elif theta >= math.pi * 5 / 2 and theta <= math.pi * 3:
        retval = 0.3 * math.cos(2 * theta + math.pi / 2) + 0.7

    return 255 * retval

def rainbow(speed=1,normalize=(1,1,1),brightness=default_brightness_ftn):
    '''Send rainbow to LED REST API'''
    for i in color_wheel.frange(0,360,0.5):
        result = color_wheel.get(i,True,"sine",normalize)
        rgb = tuple(brightness(i) * x for x in result)
        print(i,",",rgb,",",brightness(i))
        led_server_api.set(rgb)
        time.sleep(0.01 / speed)

if __name__ == "__main__":
    while True:

        rainbow(speed = 200, normalize = (1,1,1), brightness = lambda theta: ((128/180)* abs(theta - 180) + 96))



'''
        #for i in color_wheel.frange(340.0,360.0,0.5):
        for i in color_wheel.frange(65,100,0.95):
            result = color_wheel.get(i,True,"sine")
            rgb = tuple(196 * x for x in result)
            #rgb = (0,0,rgb[2])
            rgb = (rgb[0],0,0)
            print(i," , ",rgb)
            led_server_api.set(rgb)
            time.sleep(0.005)
        time.sleep(0.5) #0.01
        #time.sleep(1)
'''
