import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIR_PIN = 7

GPIO.setup(PIR_PIN, GPIO.IN)

print("PIR Module Test")

time.sleep(2)

print("Ready")

def motion(PIR_PIN):
    print("Movement detected!")


try:
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion)
    while True:
        time.sleep(100)
#    while True:
#        if GPIO.input(PIR_PIN):
#            print("Motion detected.")
#        time.sleep(1)
        
except KeyboardInterrupt:
    print ("Quit!")
    GPIO.cleanup()
    
