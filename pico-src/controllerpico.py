# Class allowing control of Pico pins with same interface
# as MCP23008

from machine import Pin, I2C

class ControllerPico:
    def __init__(self):
        # Use to hold pins - uses dictionary as not all pins used
        self.pins = {}
    
    # methods to emulate MCP23008 on the Pico
    def setPinDir(self, i, direction):
        # If existing
        #if i in pins:
        # If input (direction = 1)
        if direction == 1:
            self.pins[i] = Pin(i, Pin.IN)
        else:
            self.pins[i] = Pin(i, Pin.OUT)
            
    # Setup pull-up - most be defined as an input first
    def setPullupOn(self, i):
        self.pins[i].pull(Pin.PULL_UP)
        
    def setPinLow(self, i):
        self.pins[i].low()
        
    def setPinHigh(self, i):
        self.pins[i].high()

# Set first 4 to inputs with pull-ups 

# for i in range (0, 4):
# 
#     exp1.setPinDir(i, 1)
#     exp1.setPullupOn(i)
# 
# 
# # Set next 4 pins to outputs - set low (turn LEDs on)
# 
# for i in range (4, 8):
# 
#     exp1.setPinDir(i, 0)
# 
#     exp1.setPinLow(i)
# 
#     exp2.setPinDir(i, 0)
# 
#     exp2.setPinLow(i)
# 
#     
# 
# # Read inputs
# 
# for i in range (0, 4):
# 
#     print (f"Pin A{i} is {exp1.readPin(i)}")
# 
#     print (f"Pin B{i} is {exp2.readPin(i)}")
# 