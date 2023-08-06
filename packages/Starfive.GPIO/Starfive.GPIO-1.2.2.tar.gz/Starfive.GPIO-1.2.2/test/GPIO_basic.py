import Starfive.GPIO as GPIO
import time

GPIO.setup(0, GPIO.OUT)
GPIO.output(0, GPIO.HIGH)
time.sleep(5)
GPIO.output(0, GPIO.LOW)

GPIO.setup(1, GPIO.IN)
input_value = GPIO.input(1)
print("The input_value is {}".format(input_value))

