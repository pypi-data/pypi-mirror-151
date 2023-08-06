import Starfive.GPIO as GPIO
import time
import sys

def main():
    th1 = GPIO.TH()
    ret = th1.start()
    if (ret < 0):
        return

    th1.reset()
    i = 0
    while i < 5:
        tem = th1.getTem()
        hum = th1.getHum()
        print("Temperature = {:.2f}℃, Humidity = {:.2f} % \n".format(tem, hum))
        i = i + 1

    th1.stop()

if __name__ == "__main__":
    sys.exit(main())


