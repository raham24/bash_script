import time
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

#Number of servos
nbPCAServo=2 

#Parameters
MIN_IMP  =[500, 500]
MAX_IMP  =[2500, 2500]
MIN_ANG  =[0, 0]
MAX_ANG  =[180, 120]

#Objects (We have a 16 channel servo controller)
pca = ServoKit(channels=16)

# setup GPIO
GPIO.setmode(GPIO.BCM)  #to use the BCM pin numbers
GPIO.setwarnings(False) #ignore warnings

#initialize inputs for joysticks
CTR = 7
A = 8
B = 9
C = 10
D = 11
BUZ = 4

# setup inputs and outputs
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(A,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(B,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(C,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(D,GPIO.IN,GPIO.PUD_UP)

GPIO.setup(BUZ,GPIO.OUT)

# functions for buzzer

def beep_once():
    GPIO.output(BUZ,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZ,GPIO.LOW)

# function init 
def init():

    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])


# function main 
def center():

    #pcaScenario();
    
    pca.servo[0].angle = 62
    time.sleep(1)
    pca.servo[1].angle = 72
    time.sleep(1)
    pca.servo[0].angle=None
    time.sleep(0.5)
    pca.servo[1].angle=None
    time.sleep(0.5)

# function pcaScenario 
def servo_test():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(MIN_ANG[i],MAX_ANG[i],1):
            #print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        for j in range(MAX_ANG[i],MIN_ANG[i],-1):
            #print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)

def stop_servo():
    pca.servo[0].angle=None
    time.sleep(0.01)
    pca.servo[1].angle=None 
    time.sleep(0.01)

def center(X,Y):
    pca.servo[0].angle = 62 #angle specific to our servo to center it
    time.sleep(0.3)
    pca.servo[1].angle = 72 #angle specific to out servo to center it
    time.sleep(0.3)
    if X != 62:
        X = 62
    if Y != 72:
        Y = 72
    stop_servo()
    return X,Y

if __name__ == '__main__':
    crnt_angleX = 0
    crnt_angleY = 0
    init()
    servo_test()
    crnt_angleX, crnt_angleY = center(crnt_angleX, crnt_angleY);
    print("Tesing Complete use the Joystick to control the camera")
    
    try:
        while True:
            if GPIO.input(CTR) == 0:
                print("Centering Servo Positions")
                crnt_angleX,crnt_angleY = center(crnt_angleX,crnt_angleY)
                beep_once();
                time.sleep(1)
            elif GPIO.input(A) == 0:
                if crnt_angleY > 0:
                    print("Moving Up")
                    pca.servo[1].angle = crnt_angleY-1
                    crnt_angleY -= 1
                    stop_servo();
                    time.sleep(0.01)
                else:
                    print("Can't move down, max position reached")
                #beep_once();
            elif GPIO.input(D) == 0:
                if crnt_angleY < 120:
                    print("Moving Down")
                    pca.servo[1].angle = crnt_angleY+1
                    crnt_angleY += 1
                    stop_servo();
                    time.sleep(0.01)
                else:
                    print("Can't move left, max position reached")
            elif GPIO.input(C) == 0:
                if crnt_angleX < 180:
                    print("Moving Left")
                    pca.servo[0].angle = crnt_angleX+1
                    crnt_angleX += 1
                    stop_servo();
                    time.sleep(0.01)
                else:
                    print("Can't move right, max position reached")
            elif GPIO.input(B) == 0:
                if crnt_angleX > 0:
                    print("Moving Right")
                    pca.servo[0].angle = crnt_angleX-1
                    crnt_angleX -= 1
                    stop_servo();
                    time.sleep(0.01)
                else:
                    print("Can't move right, max position reached")
    
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()
