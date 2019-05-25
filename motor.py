import RPi.GPIO as GPIO
import time

button1_pin = 11
button2_pin = 13
reed1_pin = 15
reed2_pin = 16
m1_pin = 18
m2_pin = 22
relay_pin = 32

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(m1_pin, GPIO.OUT)
GPIO.setup(m2_pin, GPIO.OUT)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(reed1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reed2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def stop_door():
    GPIO.output(m1_pin, False)
    GPIO.output(m2_pin, False)
    GPIO.output(relay_pin, False)

closed = False
opened = True

def close_door():
    while True:
        if GPIO.input(reed1_pin):
            GPIO.output(relay_pin, True)
            GPIO.output(m1_pin, False)
            GPIO.output(m2_pin, True)
##        print("closing door!")
            if not GPIO.input(button1_pin) or not GPIO.input(button2_pin):
                stop_door()
                break
            if not GPIO.input(reed1_pin):
                time.sleep(.7)
##            print("Stopping!")
                stop_door()
                break
        else:
            print("door already closed")
            stop_door()
            break

def open_door():
    while True:
        if GPIO.input(reed2_pin):
            GPIO.output(relay_pin, True)
            GPIO.output(m1_pin, True)
            GPIO.output(m2_pin, False)
##        print("opening door!")
            if not GPIO.input(button1_pin) or not GPIO.input(button2_pin):
                stop_door()
                break
            if not GPIO.input(reed2_pin):
                time.sleep(.35)
                stop_door()
                break
        else:
            print("door already open")
            stop_door()
            break

def button(x):
    if GPIO.input(x) == 0:
        print("button {} pressed".format(x))
        return True

def reed_pin(x):
    if GPIO.input(x) == 0:
##        print("reed pin {} pressed".format(x))
        return True
    

if __name__ == "__main__":
    try:
        while True:
            if GPIO.input(button1_pin) == 0:
                print("button 1 pressed")
                time.sleep(.1)
            if GPIO.input(button2_pin) == 0:
                print("button 2 pressed")
                time.sleep(.1)
            if GPIO.input(reed1_pin) == 0:
                print("reed 1 pressed")
                time.sleep(.1)
            if GPIO.input(reed2_pin) == 0:
                print("reed 2 pressed")
                time.sleep(.1)

                
                
        
    finally:
        GPIO.cleanup()
