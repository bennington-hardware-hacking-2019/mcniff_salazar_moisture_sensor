#!/usr/bin/python3

#
# miniproj.py - we use a soil moisture sensor
# Authors: Anna McNiff and Emma Salazar
# Date: 4/17/19
#

# import stuff
import smbus
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time

# numbers for display
numbers = [0x003F, 0x0006, 0x005B, 0x004F, 0x0066, 0x006D, 0x007D, 0x0007, 0x007F, 0x006F]
numbers_with_decimal = [0x00BF, 0x0086, 0x00DB, 0x00CF, 0x00E6, 0x00ED, 0x00FD, 0x0087, 0x00FF, 0x00EF]
negative = [0x0040]

# seven segment display information
DISPLAY_ADDRESS = 0x0070
DISPLAY_SETUP = 0x0081
DISPLAY_OFF = 0x0080
DISPLAY_REGISTER1 = 0x0000
DISPLAY_REGISTER2 = 0x0002
DISPLAY_REGISTER3 = 0x0006
DISPLAY_REGISTER4 = 0x0008
DISPLAY_SYSTEM_REGISTER = 0X0021

# adc information
ADC_ADDRESS = 0x0048
ADC_CONFIG_REGISTER = 0X0001
ADC_CONVERSION_REGISTER = 0X0000

# ?
bus = smbus.SMBus(1)

config_bytes = [ 0x00C2, 0x0081 ]

# adc functions
def configure_adc(my_bus):
	my_bus.write_i2c_block_data(ADC_ADDRESS, ADC_CONFIG_REGISTER, config_bytes)

def get_raw_reading(my_bus):
	raw_reading = my_bus.read_i2c_block_data(ADC_ADDRESS, ADC_CONVERSION_REGISTER)
	MSB = raw_reading[0] <<8
	RAW_MOISTURE = MSB + raw_reading[1]
	return RAW_MOISTURE

configure_adc(bus)

# seven segment display functions
def turn_on_unit(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_SYSTEM_REGISTER)

def turn_on_display(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_SETUP)

def turn_off_display(my_bus):
	my_bus.write_byte(DISPLAY_ADDRESS, DISPLAY_OFF)

def num_on_thousands(my_bus):
	blank = negative[0]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER1, blank)

def num_on_hundreds(my_bus):
	blank = negative[0]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER2, blank)

def num_on_tens(my_bus, tens):
	number = numbers[tens]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER3, number)
	#print(number)

def num_on_ones(my_bus, ones):
	number = numbers[ones]
	my_bus.write_byte_data(DISPLAY_ADDRESS, DISPLAY_REGISTER4, number)
	#print(number)

# soil sensor stuff
GPIO.setup(11, GPIO.OUT)			#sets up the GPIO pin that is connected to our sensor

def turn_on_soil_sensor():
	GPIO.output(11, GPIO.HIGH)
#	time.sleep(0.5)
#	GPIO.output(11, GPIO.LOW)

turn_on_soil_sensor()
my_raw_reading = get_raw_reading(bus)
turn_on_unit(bus)
turn_on_display(bus)

print(my_raw_reading)

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

time.sleep(5)

turn_off_display(bus)
