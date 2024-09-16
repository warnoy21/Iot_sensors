######################################################
# IoT that uses UART receiver using raspberry pi GPIO 10 (RX) to receive
#data from STM32F411RE to decide the status of a wemo plug switch
#
# Created by    Aaron Gumba         Date: September 16, 2024
#
#####################################################3

import serial
import RPi.GPIO as GPIO
import pywemo
import time

# GPIO pins for the serial and wemo LED
SERIAL_PIN = 16
WEMO_PIN = 12

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERIAL_PIN, GPIO.OUT)
GPIO.setup(WEMO_PIN, GPIO.OUT)

GPIO.output(SERIAL_PIN, GPIO.LOW)  # Turn off serial LED initially
GPIO.output(WEMO_PIN, GPIO.LOW)
# Discover Wemo devices on the network
devices = pywemo.discover_devices()

# Check if any devices 
if devices:
    GPIO.output(WEMO_PIN, GPIO.HIGH)  # Turn on the LED to indicate devices found
    wemo_outlet = devices[0]  # first device found
    wemo_outlet.on()
else:
    
    GPIO.output(WEMO_PIN, GPIO.LOW)  # Keep the LED off if no devices are found
    


# Configure the serial port matching the STM32's UART configuration
ser = serial.Serial(
    port='/dev/serial0',  
    baudrate=9600,        
    parity=serial.PARITY_NONE,  
    stopbits=serial.STOPBITS_ONE,  
    bytesize=serial.EIGHTBITS,  
    timeout=1  
)

# Ensure the serial port is open
if ser.isOpen():
    GPIO.output(SERIAL_PIN, GPIO.HIGH)  

try:
    while True:
        # Read data from UART
        if ser.in_waiting > 0:  # Check if any data is available
            received_data = ser.read(ser.in_waiting).decode('utf-8', errors='replace')
            if received_data == 'O':
                wemo_outlet.off()

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    # Close the serial port 
    ser.close()
    print("Serial port closed.")
    GPIO.output(SERIAL_PIN, GPIO.LOW)  
    GPIO.cleanup() 

