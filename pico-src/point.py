# Module for point controller
# Each of the items are a tuple having the controller followed by port

from utime import sleep

# LEDs are 1 for on and 0 for off
# Electrically they are opposite (sink) so when calling controller invert state

class Point:
        
    def __init__(self, controller, point0, point1, switch0, switch1, led0, led1 ):
        self.controller = controller
        self.points = [point0, point1]
        self.switches = [switch0, switch1]
        self.leds = [led0, led1]
        
    # Set both LEDs to off
    def unknown(self):
        self.set_led(0, 0)
        self.set_led(1, 0)
        
    # Sets the point LED - and triggers movement
    def set_point(self, position):
        # Position 0 is unknown, position 1 is up, position 2 is down
        # Set LED first
        if (position == 0):
            self.unknown()
        elif (position == 1):
            self.set_led(0, 1)
            self.set_led(1, 0)
            self.switch_point(self.points[0])
        else:
            self.set_led(0, 0)
            self.set_led(1, 1)
            self.switch_point(self.points[1])
        
        
    # Set point on, wait for .3sec then back off
    def switch_point (self, point_addr):
        self.controller.set_pin(point_addr, 1)
        sleep(0.3)
        self.controller.set_pin(point_addr, 0)
        
    # Sets an individual LED
    # 1 = on, 0 = off
    def set_led(self, led_num, state):
        # invert with controller
        # convert to address instead of led number
        self.controller.set_pin(self.leds[led_num], 1 - state)
        
    # Return a list of all inputs
    def get_inputs (self):
        return self.switches
    
    # Return a list of all outputs (points and LEDs)
    def get_outputs (self):
        list = self.points
        list.extend(self.leds)
        return list
    
    # Returns 0 for none 1 for switch0 and 2 for switch1
    # 2 is up or left, 1 is down or right, 0 is none
    def switch_position (self):
        # Only check for first status it's a toggle switch
        if (self.controller.get_pin(self.switches[0]) == 0):
            return 2
        elif (self.controller.get_pin(self.switches[1]) == 0):
            return 1
        else:
            return 0

