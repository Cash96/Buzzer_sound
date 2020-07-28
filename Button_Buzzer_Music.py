import RPi.GPIO as GPIO
import time
import BMC

#watch for warnings
GPIO.setwarnings(False)

#Set up buzzer pin
buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

#set up PWM
DutyCycle = 1
p = GPIO.PWM(buzzer_pin, 1)


buttons = BMC.ButtonMatrix()

def ChangeSound(B):
    if B == 0:
        print("Changing frequency to 5")
        p.ChangeFrequency(20)
        DutyCycle = 5
    elif B == 1:
        print("Changing frequency to 90")
        p.ChangeFrequency(200)
        DutyCycle = 10
    elif B == 2:
        print("Changing frequency to 90")
        p.ChangeFrequency(400)
        DutyCycle = 20
        
try:
    while(True):
        for j in range(len(buttons.columnPins)):
            # set each output pin to low
            GPIO.output(buttons.columnPins[j],0)
            for i in range(len(buttons.rowPins)):
                if GPIO.input(buttons.rowPins[i]) == 0:
                    # button pressed, activate it store the value
                    btn = buttons.activateButton(i,j)
                    print("hello pin number {}".format(btn +1))
                    ChangeSound(btn)
                    p.start(DutyCycle)
                    while buttons.buttonHeldDown(i):
                        p.start(DutyCycle)
                    p.stop()
            # return each output pin to high
            GPIO.output(buttons.columnPins[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()
