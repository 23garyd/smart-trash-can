import os
from clarifai.rest import ClarifaiApp
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
from adafruit_servokit import ServoKit
import time

LedGPIO = 17    # pin11 --- led
BtnGPIO = 18    # pin12 --- button
kit = ServoKit(channels=16)
camera = PiCamera()

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LedGPIO, GPIO.OUT)
	GPIO.setup(BtnGPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedGPIO, GPIO.HIGH)
	
setup()

# Instantiate a new Clarifai app by passing in your API key.
app = ClarifaiApp(api_key='8e3dc665a6c74e9daf5473b94971ae0a')
# Choose one of the public models.
model = app.public_models.general_model
recyclelist = ['recycling', 'glass', 'paper', 'metal', 'cardboard', 'plastic', 'bottle', 'can', 'carton', 'reflection',
'compartment','glass items', 'H2O']

trashlist = ['trash', 'wrapping', 'banana', 'orange', 'bag', 'wrapper', 'balloon', 'rubber', 'shoe', 'straw', 'tube', 
'medicine', 'light bulb', 'bulb', 'pumpkin', 'food', 'fruit', 'trash', 'footwear', 'sneakers' ]


while True:

	if GPIO.input(BtnGPIO) == GPIO.LOW: # Check whether the button is pressed or not.
		GPIO.output(LedGPIO, GPIO.LOW)   
		print('button press detected...scanning image')
		camera.capture('clarifai.jpg')
		# Predict the contents of an image by passing in a URL.
		#response = model.predict_by_url(url='https://samples.clarifai.com/metro-north.jpg')
		response = model.predict_by_filename('clarifai.jpg')
		#print(response)
		#print(response['outputs'][0]['data']['concepts'][0]['name']
		kit.servo[15].angle = 90
		time.sleep(1)
		for i in range(len(response['outputs'][0]['data']['concepts'])):
			testname = response['outputs'][0]['data']['concepts'][i]['name']
			print(testname)			
			if testname in recyclelist:
				print("recycling")
				kit.servo[15].angle = 180
				time.sleep(5)
				kit.servo[15].angle = 90
				break
			elif testname in trashlist:
				print("trash")
				kit.servo[15].angle = 0
				time.sleep(5)
				kit.servo[15].angle = 90
				break
			else:
				print("nothing found")
		print("for loop end")
	else:
		GPIO.output(LedGPIO, GPIO.HIGH)  
		print("no action detected")
