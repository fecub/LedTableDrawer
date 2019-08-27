import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# init list with pin numbers

DEFUSEPIN = 7  

GPIO.setup(DEFUSEPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# pinList = [2, 3, 4, 17, 27, 22, 10, 9]
# pinList = [29,31,33,35,37,32,36,38]
pinList = [5,20,26,19,6,12,16,21] # 13 20

# loop through pins and set mode and state to 'low'

for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)

# time to sleep between operations in the main loop

SleepTimeL = 0.2

# main loop
i1=0
while True:
    GPIO.output(5, GPIO.LOW)
    print "ONE"
    # time.sleep(SleepTimeL); 

    if(GPIO.input(DEFUSEPIN)):
        print("Kabel 1 wurde ",i1, " x reingesteckt")
        i1=i1+1

    
    time.sleep(1)


try:
    # GPIO.output(5, GPIO.LOW)
    # print "ONE"
    # time.sleep(SleepTimeL); 
    # GPIO.output(20, GPIO.LOW)
    # print "TWO"
    # time.sleep(SleepTimeL);  
    # GPIO.output(26, GPIO.LOW)
    # print "THREE"
    # time.sleep(SleepTimeL)
    # GPIO.output(19, GPIO.LOW)
    # print "FOUR"
    # time.sleep(SleepTimeL)
    # GPIO.output(6, GPIO.LOW)
    # print "FIVE"
    # time.sleep(SleepTimeL)
    # GPIO.output(12, GPIO.LOW)
    # print "SIX"
    # time.sleep(SleepTimeL)
    # GPIO.output(16, GPIO.LOW)
    # print "SEVEN"
    # time.sleep(SleepTimeL)
    # GPIO.output(21, GPIO.LOW)
    # print "EIGHT"
    # time.sleep(SleepTimeL)

    # GPIO.output(5, GPIO.HIGH)
    # print "ONE"
    # time.sleep(SleepTimeL); 
    # GPIO.output(20, GPIO.HIGH)
    # print "TWO"
    # time.sleep(SleepTimeL);  
    # GPIO.output(26, GPIO.HIGH)
    # print "THREE"
    # time.sleep(SleepTimeL)
    # GPIO.output(19, GPIO.HIGH)
    # print "FOUR"
    # time.sleep(SleepTimeL)
    # GPIO.output(6, GPIO.HIGH)
    # print "FIVE"
    # time.sleep(SleepTimeL)
    # GPIO.output(12, GPIO.HIGH)
    # print "SIX"
    # time.sleep(SleepTimeL)
    # GPIO.output(16, GPIO.HIGH)
    # print "SEVEN"
    # time.sleep(SleepTimeL)
    # GPIO.output(21, GPIO.HIGH)
    # print "EIGHT"
    # time.sleep(SleepTimeL)

    # GPIO.output(21, GPIO.HIGH)
    # print "ONE"
    # time.sleep(SleepTimeL); 
    # GPIO.output(16, GPIO.HIGH)
    # print "TWO"
    # time.sleep(SleepTimeL);  
    # GPIO.output(12, GPIO.HIGH)
    # print "THREE"
    # time.sleep(SleepTimeL)
    # GPIO.output(6, GPIO.HIGH)
    # print "FOUR"
    # time.sleep(SleepTimeL)
    # GPIO.output(19, GPIO.HIGH)
    # print "FIVE"
    # time.sleep(SleepTimeL)
    # GPIO.output(26, GPIO.HIGH)
    # print "SIX"
    # time.sleep(SleepTimeL)
    # GPIO.output(20, GPIO.HIGH)
    # print "SEVEN"
    # time.sleep(SleepTimeL)
    # GPIO.output(5, GPIO.HIGH)
    # print "EIGHT"
    # time.sleep(SleepTimeL)
    GPIO.cleanup()
    print "Good bye!"

# End program cleanly with keyboard
except KeyboardInterrupt:
  print "  Quit"

  # Reset GPIO settings
  GPIO.cleanup()