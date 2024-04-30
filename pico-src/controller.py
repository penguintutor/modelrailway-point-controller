# This assumes that there are two MCP23008 connected to pins 4 & 5 of Pico
# First has all addresses to 0 = address 32, second has a0 to 1 = address 33
# Also needs mcp23008.py from:
# https://github.com/CrankshawNZ/Micropython/blob/master/mcp23008.py

from machine import Pin, I2C
from mcp23008 import MCP23008
from controllerpico import ControllerPico

class Controller:
    
    # Uses addresses - for Pico use address 0, controllers use address
    # I2C address should be (id, scl, sda) eg. (0,5,4)
    def __init__(self, i2c_address, controller_addresses):
        self.controller_address = controller_addresses
        self.controller = []

        i2c = I2C(id=i2c_address[0], scl=Pin(i2c_address[1]), sda=Pin(i2c_address[2]), freq=100000)
        
        print ("I2C Scan")
        print (i2c.scan())
        
        #print ("Hex version")
        #addrs = [hex(addr) for addr in i2c.scan()]
        #print(addrs)

        for this_controller in self.controller_address:
            if this_controller == 0:
                # Create a Pico device
                self.controller.append(ControllerPico())
            else:
                self.controller.append(MCP23008(i2c, this_controller))

    def set_inputs (self, inputs):
        for this_input in inputs:
            self.controller[this_input[0]].setPinDir(this_input[1], 1)
            # Also set pullup
            self.controller[this_input[0]].setPullupOn(this_input[1])
                
    def set_outputs (self, outputs):
        for this_output in outputs:
            self.controller[this_output[0]].setPinDir(this_output[1], 0)
            # Set to low
            self.controller[this_output[0]].setPinLow(this_output[1])
            
    # State = 1 for high and 0 for low (note that LEDs are opposite - see point.py)
    def set_pin (self, addr, state):
        if state == 1:
            self.controller[addr[0]].setPinHigh(addr[1])
        else:
            self.controller[addr[0]].setPinLow(addr[1])

    def get_pin (self, addr):
        return self.controller[addr[0]].readPin(addr[1])
    
    # Depreciated - use get_pin instead
    def get_input (self, addr):
        return self.controller[addr[0]].readPin(addr[1])
        
    


# Read inputs
#for i in range (0, 4):
#    print (f"Pin A{i} is {exp1.readPin(i)}")
