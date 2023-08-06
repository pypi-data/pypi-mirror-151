import Starfive.GPIO as GPIO
import sys
import time

DIN = 0
CS  = 2
CLK = 4

GPIO.setup(DIN, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)

buffer = ['01111000', '01000000', '01111000', '01001111', '01111001', '00001111', '000000001', '00001111']

buffer_off = ['0', '0', '0', '0', '0', '0', '0', '0']

def sendbyte(bytedata):
    for bit in range(0, 8):
        if ((bytedata << bit) & 0x80):
            GPIO.output(DIN, GPIO.HIGH)
        else:
            GPIO.output(DIN, GPIO.LOW)

        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)


def WriteToReg(regaddr, bytedata):
    GPIO.output(CS, GPIO.HIGH)
    GPIO.output(CS,GPIO.LOW)
    GPIO.output(CLK, GPIO.LOW)
    sendbyte(regaddr)
    sendbyte(bytedata)
    GPIO.output(CS, GPIO.HIGH)

def WriteALLReg():
    time.sleep(0.1)
    for i in range(0, 8):
        WriteToReg(i+1, int(buffer[i], 2))
    time.sleep(5)

    for i in range(0, 10):
        for i in range(0, 8):
            WriteToReg(i+1, int(buffer_off[i], 2))
        time.sleep(0.1)
        for i in range(0, 8):
            WriteToReg(i+1, int(buffer[i], 2))
        time.sleep(0.1)

def initData():
    WriteToReg(0x09, 0x00) # set decode mode
    WriteToReg(0x0a, 0x03) # set brightness
    WriteToReg(0x0b, 0x07) # set scan limit
    WriteToReg(0x0c, 0x01) # set power mode
    WriteToReg(0x0f, 0x00) 

def main():
    initData()
    while True:
        WriteALLReg()

if __name__ == "__main__":
    sys.exit(main())