import RPi.GPIO as GPIO
import time
from AlphaBot2 import AlphaBot2 # import the class with function definitions

Ab = AlphaBot2() # Ab = alphabot robot

DR = 19          # Infrared sensor Right
DL = 16          # Infrared sensor Left

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP) # set Infrared sensor as input, type PUD_UP (pull up resistor)
GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

Ab.setPWMA(20) # set duty cycle for the left motor
Ab.setPWMB(20) # set duty cycle for the right motor

# Duty cycle is used to set the speed of the robot
# Recomended duty cycle is anywhere between 20-30
 
try: # catch runtime error in the block of code inside try
        Ab.forward() # start moving forward slowly

        while True: # run forever
        
                DR_status = GPIO.input(DR) # read again the infrared sensors
                DL_status = GPIO.input(DL)

                if DR_status == 0 or DL_status == 0:
                        Ab.stop()
                        if DR_status == 0: #if the right sensor reads 0, move left
                                print("Object on right, moving left")
                                Ab.left()
                                time.sleep(0.1)
                                Ab.stop()
                        if DL_status == 0: #if the left sensor reads 0, move right
                                print("Object on left, moving right")
                                Ab.right()
                                time.sleep(0.1)
                                Ab.stop()
                else:
                        Ab.forward()
                         
except KeyboardInterrupt: # if the program was stopped from the keyboard (ctrl-c) then stop the program 
        GPIO.cleanup();
