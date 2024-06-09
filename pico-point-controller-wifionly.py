# Code for controlling Model Railway points
# Point controller board
# Also needs secrets.py with WiFi login details
# For more details see: https://www.penguintutor.com/points

# Alternative to pico-point-controller.py to allow testing of
# main board without being connected to add-on switch board

from machine import Pin
from utime import sleep
import network
import socket
import uasyncio as asyncio
import secrets
import re
from url_handler import URL_Handler
from pixelstatus import *
from point import Point
from controller import Controller

# Mode can be ap (access point where the Pico acts as a web server)
# or "client" [default] which connects to an existing network
# Note that client mode is blocking and will not run the rest of the code
# until a network connection is established
mode="client"

# Do we display light sequence on startup - helpful to test if working
intro = True

# All documents in DocumentRoot are publically accessible
DocumentRoot = "public/"

# If ip_config not blank then use for network config
# otherwise set to "" to use dhcp
ip_config = ("192.168.0.53", "255.255.255.0", "192.168.0.1", "8.8.8.8")

# Indexed at 0 (board labelling is 1)

controller = Controller((0,5,4), (0, 32, 33), i2c_control=False)

# Each of the points is created as an instance of point object
# Each of the pins is given a tuple representing controller number, followed by port number
# Pico is controller 0, MCP23008 are 1 and 2
# Point class uses controller, point0, point1, switch0, switch1, led0, led1
points = [
    Point(controller, (0,6), (0, 7), (1,0), (1,1), (1,4), (1,5)),
    Point(controller, (0,8), (0, 9), (1,2), (1,3), (1,6), (1,7)),
    Point(controller, (0,10), (0, 11), (2,0), (2,1), (2,4), (2,5)),
    Point(controller, (0,12), (0, 13), (2,2), (2,3), (2,6), (2,7))
]



url = URL_Handler(DocumentRoot)

      
def connect():
    #Connect to WLAN
    if mode== "ap":
        # Access Point mode
        ip = connect_ap_mode()
    else:
        ip = connect_client_mode()
    return ip
    


def connect_ap_mode ():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=secrets.SSID, password=secrets.PASSWORD)
    wlan.active(True)
    while wlan.active() == False:
        print ('Trying to setup AP mode')
    ip = wlan.ifconfig()[0]
    print('AP Mode is active')
    print('Connect to Wireless Network '+secrets.SSID)
    print('Connect to IP address '+ip)
    return ip

def connect_client_mode ():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power saving mode
    if ip_config != "":
        wlan.ifconfig(ip_config)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connect to IP address '+ip)    
    return ip



def setup_pins ():
    # List of inputs and outputs used in setup
    inputs = []
    outputs = []

    # Setup inputs and outputs
    for this_point in points:
        inputs.extend(this_point.get_inputs())
        outputs.extend(this_point.get_outputs())
    # Wifi only no inputs - next line commented out
    controller.set_inputs(inputs)
    controller.set_outputs(outputs)
    
    # Set all points to unknown state (both LEDs off)
    for this_point in points:
        this_point.unknown()
        
    if intro == True:
        # Quick flash intro
        for this_point in points:
            this_point.set_led(0, 1)
            sleep(0.5)
            this_point.set_led(0, 0)
            this_point.set_led(1, 1)
            sleep(0.5)
            this_point.set_led(1, 0)
            

async def serve_client(reader, writer):
    status_active()
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = request_line.decode("utf-8")
    
    # point change request (returns own string)
    point_change = url.change_point(request)
    if point_change != None:
        if (point_change[1] == 1):
            points[point_change[0]].set_point(1)
        elif (point_change[1] == 2):
            points[point_change[0]].set_point(2)
        # Ignore any other values (code doesn't support any)
        # Return status - currently just text (will change to JSON)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/text\r\n\r\n')
        writer.write('Status ...')
    
    
    else:
        # Otherwise is this is static file request
        
        url_value, url_file, url_type = url.validate_file(request)

        writer.write('HTTP/1.0 {} OK\r\nContent-type: {}\r\n\r\n'.format(url_value, url_type))
        # Send file 1kB at a time (avoid problem with large files exceeding available memory)
        with open(DocumentRoot+url_file, "rb") as read_file:
            data = read_file.read(1024)
            while data:
                writer.write(data)
                await writer.drain()
                data = read_file.read(1024)
            read_file.close()

    await writer.wait_closed()
    print("Client disconnected")

    status_ready()

# Initialise Wifi
async def main ():
    # Set Status LED to Red (power on)
    status_power()
    setup_pins ()
    print ("Connecting to network")
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset
    print ("IP address", ip)
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print ("Web server listening on", ip)
    status_ready()
    while True:
        #onboard.on()
        # Enable following line for heartbeat debug messages
        #print ("heartbeat")
        await asyncio.sleep(0.25)
        # Check gpio pins 10 times between checks for webpage (5 secs)
        for i in range (0, len(points)):
            #print (f"Switch {i} is {points[i].switch_position()}")
            pos = points[i].switch_position()
            if (pos == 0):
                # ignore
                pass
            else:
                points[i].set_point(pos)
                
#        for i in range (0, 5):
#            check_gpio_buttons()
    



if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()