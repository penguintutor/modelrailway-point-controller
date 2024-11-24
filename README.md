# Model railway point controller

The model railway point controller provides a way to control up to 4 points using a Raspberry Pi Pico W. It includes a MOSFET based capacitor discharge unit on the PCB and MOSFET controllers for each of the point motors.

It includes a second control board connected by I2C which can be connected to physical LEDs and switches to provide a way to control the points. The points can also be controlled using a web interface which can also be used in conjunction with GUI software to provide a touch screen interface.

# Installation

This version needs to be installed on a Raspberry Pi Pico W with the appropriate network enabled MicroPython. MicroPython can be installed through the Thonny editor.

To install the program, copy all the files in the pico-src directory to the top-level of the Raspberry Pi Pico. For the network connection you also need to create a file called secrets.py with details of your SSID and PASSWORD. The example below shows the formatting for the secrets.py file.

    SSID="NetworkSSID"
    PASSWORD="WiFiPassword"
    
## Configuration

The program can be run in two modes. 

* Access Point Mode (AP mode) - In this mode the Pico will act as a Wireless Access Point which you can connect to using another WiFi enabled device.
* Client Mode - In this mode you can connect to an existing wireless network

Note that in client mode it is currently blocking and will not operate until it has successfully connected to the network.

The mode is set by editing the entry "mode" in the pico-lights.py file. 

mode="ap"       # Use as an access point
mode="client"   # Use as a Wi-Fi client

    
## Running on startup

For the code to run automatically on start-up save the pico-point-controller.py file on your Pico as main.py.

# More Information

For more details see [www.penguintutor.com/points](https://www.penguintutor.com/points)

