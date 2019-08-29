import serial
import time
 
#s = serial.Serial() # Namen ggf. anpassen
#s = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
s = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#s.open()
time.sleep(5) # der Arduino resettet nach einer Seriellen Verbindung, daher muss kurz gewartet werden


# a 7.5s, explosion
# c  42s, tic tac
# f   8s, win
while True:
    print("starting")
    s.write(str.encode('c'))
    time.sleep(42.2)

#s.write("a")
#time.sleep(5)
#s.write("-")
#s.write("a")
#s.write("b")
#time.sleep(5)
#s.write("c")
#time.sleep(5)
#s.write("d")
#time.sleep(5)
#s.write("e")
#time.sleep(5)
#s.write("f")
#time.sleep(5)

#try:
#    while True:
#        response = s.readline()
#        print(response)
#except KeyboardInterrupt:
#    s.close()
