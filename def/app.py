import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BOARD)

DEFUSEPIN1 = 35
DEFUSEPIN2 = 37

GPIO.setup(DEFUSEPIN1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(DEFUSEPIN2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def main():
    i1=0
    i2=0
    while True:
        if(GPIO.input(DEFUSEPIN1)):
            print("Kabel 1 wurde ",i1, " x reingesteckt")
            i1=i1+1
        if(GPIO.input(DEFUSEPIN2)):
            print("Kabel 2 wurde ",i2, " x reingesteckt")
            i2=i2+1
        
        time.sleep(1)

if __name__ == "__main__":
    main()