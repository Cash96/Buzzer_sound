#Import tools
import RPi.GPIO as GPIO    #control the GPIO pins with code
import BMC                 #custom class file to control button matrix

#watch for warnings
GPIO.setwarnings(False)

#Set up buzzer pin
buzzer_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)

#set up PWM
DutyCycle = 1               #Duty cycle can be 1-99 in value
p = GPIO.PWM(buzzer_pin, 1)

#create a button matrix object
buttons = BMC.ButtonMatrix()

#A function to change the duty cycle and frequency based on the button number
#B = the button being pressed
#human frequency for hearing goes from 20-20,000
def ChangeSound(B):    
    if B == 0:
        print("Changing frequency to 300")
        p.ChangeFrequency(300)
        DutyCycle = 5
    elif B == 1:
        print("Changing frequency to 400")
        p.ChangeFrequency(400)
    elif B == 2:
        print("Changing frequency to 500")
        p.ChangeFrequency(500)
    #add more elif statements here to accomodate more buttons
        
try:
    while(True):
        for j in range(len(buttons.columnPins)):
            # set each output pin to low
            GPIO.output(buttons.columnPins[j],0)
            for i in range(len(buttons.rowPins)):
                if GPIO.input(buttons.rowPins[i]) == 0:
                    # button pressed, activate it store the value
                    btn = buttons.activateButton(i,j)  #the number button being pressed
                    ChangeSound(btn)
                    p.start(DutyCycle)
                    while buttons.buttonHeldDown(i):
                        p.start(DutyCycle)
                    p.stop()
            # return each output pin to high
            GPIO.output(buttons.columnPins[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()
