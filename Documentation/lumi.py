# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(15, GPIO.IN)

channel = 15
from neopixel import *
from firebase import *

import datetime
import argparse
import signal
import sys

def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

ts = time.asctime( time.localtime(time.time()) )
my_url = 'https://software-project-1512689251496.firebaseio.com/'
firebase = firebase.FirebaseApplication(my_url, None)

# Define functions which animate LEDs in various ways.
def callback(channel):
	if GPIO.input(15):
		print "Crying Detected!"
		cryActivity(strip)
		cryval = {"Crying Activity": ts}
		firebase.post('/sound', cryval)
		firebase.patch(my_url + '/sound', cryval)

def idle(strip, wait_ms=20, iterations=1):
	"""Draw one color."""
	for i in range(strip.numPixels()):
            strip.setBrightness(50)
            strip.setPixelColorRGB(i, 0, 0, 255)
            strip.show()
            #rgbval = {"RGB value": strip}
	    #firebase.post('/neopixel', rgbval)
            time.sleep(wait_ms/1000.0)
            
def cryActivity(strip, wait_ms=20, iterations=1):
	"""Draw one color."""
	for i in range(strip.numPixels()):
            strip.setBrightness(255)
            strip.setPixelColorRGB(i, 255, 0, 0)
            strip.show()
            #rgbval = {"RGB value": setPixelColorRGB()}
	    #firebase.post('/neopixel', strip)
            time.sleep(wait_ms/1000.0)                       

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)
	    
def ledOff():
#	time.sleep(15)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))

	strip.show()

def sigint_handler(signal, frame):
	ledOff()
	sys.exit(0)


# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	GPIO.add_event_detect(15, GPIO.BOTH, bouncetime=300)
	GPIO.add_event_callback(15, callback)
	signal.signal(signal.SIGINT, sigint_handler)

	print ('Press Ctrl-C to quit.')
	while True:
	    idle(strip)
