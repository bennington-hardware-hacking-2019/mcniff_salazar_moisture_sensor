#!/usr/bin/python3

#
# miniproj.py - A program written to utilize the SparkFun Soil Moisture Sensor. 
# https://learn.sparkfun.com/tutorials/soil-moisture-sensor-hookup-guide?_ga=2.156393023.545380768.1554317640-1658813617.1554317640#hardware-overview-and-assembly
# Authors: Anna McNiff and Emma Salazar
# Date: 4/17/19
#


# Import Stuff
import smbus
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time


# Symbols for Display
numbers = [0x003F, 0x0006, 0x005B, 0x004F, 0x0066, 0x006D, 0x007D, 0x0007, 0x007F, 0x006F]	# translated: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
negative_symbol = [0x0040]


# Seven Segment Display Information
DISPLAY_ADDRESS = 0x0070
DISPLAY_SETUP = 0x0081
DISPLAY_OFF = 0x0080
DISPLAY_REGISTER1 = 0x0000
DISPLAY_REGISTER2 = 0x0002
DISPLAY_REGISTER3 = 0x0006
DISPLAY_REGISTER4 = 0x0008
DISPLAY_SYSTEM_REGISTER = 0X0021


# ADC Information
ADC_ADDRESS = 0x0048
ADC_CONFIG_REGISTER = 0X0001
ADC_CONVERSION_REGISTER = 0X0000


# This allows us to talk to our i2c bus by creating the object "bus." 
bus = smbus.SMBus(1)			# It tells smbus to use i2c channel 1, which is what our GPIO i2c pins are working on


# A list of two bytes containing the MSB and LSB of our configuration register. 
# 0x00C2 is bits 15:8; bit 15: operational status, bit 14-12: mux config, bits 11-9: programmable gain amplifier settings, and bit 8: device operating mode; all together are set to 11000010
# 0x0081 is bits 7:0; bits 7-5: data rate, bit 4: comparator mode, bit 3: comparator polarity, bit 2: latching comparator, bits 1-0: comparator queue; all together are set to 10000011  
config_bytes = [ 0x00C2, 0x0081 ]


# ADC Functions

# this function configures our adc
def configure_adc(my_bus):
	my_bus.write_i2c_block_data(ADC_ADDRESS, ADC_CONFIG_REGISTER, config_bytes)

# this function reads a block of data from the adc, the data coming from the sensor, then combines the list of two bytes from the reading and combines them into one number, returning the raw moisture reading
def get_raw_reading(my_bus):
	raw_reading = my_bus.read_i2c_block_data(ADC_ADDRESS, ADC_CONVERSION_REGISTER)
	MSB = raw_reading[0] <<8
	RAW_MOISTURE = MSB + raw_reading[1]
	return RAW_MOISTURE

# here we call our configure_adc() function
configure_adc(bus)


# Seven Segment Display Functions

# this function turns on our seven-segment display 
def turn_on_unit(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_SYSTEM_REGISTER)

# this function turns on the actual lights on the display
def turn_on_display(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_SETUP)

# this function turns off the display
def turn_off_display(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_OFF)

# gives the first block in the display the value we want it to display
def num_on_thousands(my_bus):
	blank = negative[0]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER1, blank)

# gives the second block in the display the value we want it to display
def num_on_hundreds(my_bus):
	blank = negative[0]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER2, blank)

# gives the third block in the display the value we want it to display
def num_on_tens(my_bus, tens):
	number = numbers[tens]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER3, number)
	#print(number)

# gives the fourth block in the display the value we want it to display
def num_on_ones(my_bus, ones):
	number = numbers[ones]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER4, number)
	#print(number)


# Soil Sensor Stuff

GPIO.setup(11, GPIO.OUT)			#sets up the GPIO pin that is connected to our sensor

# this function turns on our soil sensor so it is not given constant power, to prevent corrosion of the probes.
def turn_on_soil_sensor():
	GPIO.output(11, GPIO.HIGH)
#	time.sleep(0.5)
#	GPIO.output(11, GPIO.LOW)

# calling our remaining needed functions
turn_on_soil_sensor()
my_raw_reading = get_raw_reading(bus)
turn_on_unit(bus)
turn_on_display(bus)

print(my_raw_reading)

# setting the values that get sent to the seven seg based on the raw reading from the sensor
if my_raw_reading == 0:
	num_on_tens(bus, 0)
	num_on_ones(bus, 0)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 0 < my_raw_reading < 2200:
	num_on_tens(bus, 0)
	num_on_ones(bus, 1)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 2200 < my_raw_reading < 4400:
	num_on_tens(bus, 0)
	num_on_ones(bus, 2)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 4400 < my_raw_reading < 6600:
	num_on_tens(bus, 0)
	num_on_ones(bus, 3)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 6600 < my_raw_reading < 8800:
	num_on_tens(bus, 0)
	num_on_ones(bus, 4)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 8800 < my_raw_reading < 11000:
	num_on_tens(bus, 0)
	num_on_ones(bus, 5)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 11000 < my_raw_reading < 13200:
	num_on_tens(bus, 0)
	num_on_ones(bus, 6)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 13200 < my_raw_reading < 15400:
	num_on_tens(bus, 0)
	num_on_ones(bus, 7)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 15400 < my_raw_reading < 17600:
	num_on_tens(bus, 0)
	num_on_ones(bus, 8)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 17600 < my_raw_reading < 19800:
	num_on_tens(bus, 0)
	num_on_ones(bus, 9)
	num_on_hundreds(bus)
	num_on_thousands(bus)
elif 19800 < my_raw_reading < 22000:
	num_on_tens(bus, 1)
	num_on_ones(bus, 0)
	num_on_hundreds(bus)
	num_on_thousands(bus)

# give some pause before we turn off the display
time.sleep(5)

# turn off the seven seg
turn_off_display(bus)
