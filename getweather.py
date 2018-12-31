#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib2
#import time
#import datetime
#import re
#import os

#import requests
from datetime import date, datetime, timedelta
import mysql.connector
import smbus
import RPi.GPIO as GPIO
from BME280 import *

#========================================
# Settings
#========================================
temperature_unit = 'C' # 'C' | 'F'
pressure_unit = 'mm Hg' # 'Pa' | 'mm Hg'
humidity_unit = '%'
#========================================
temperature_field = 'temperature'
pressure_field = 'pressure'
humidity_field = 'humidity'

units = {temperature_field: temperature_unit, pressure_field: pressure_unit, humidity_field: humidity_unit}

def convert(value, unit):
	if unit == 'F':
		# Convert from Celsius to Fahrenheit
		return round(1.8 * value + 32.0, 2)
	if unit == 'mm Hg':
		 #Convert from Pa to mm Hg
		return round(value * 0.00750061683, 2)
	return value
print "Date: ",datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
print('11 pin Off')
GPIO.output(11, False) # записываем в GPIO 11 “1” (3.3 V)
time.sleep(1)
print('11 pin On')
GPIO.output(11, True) # записываем в GPIO 11 “0” (0 V)
time.sleep(5)

port = 1
default_i2c_hub_address = 0x70
bus = smbus.SMBus(port)
bus.write_byte(default_i2c_hub_address, 0)
#for i in range(255):
#print i
cnx = mysql.connector.connect(user='PrintUser', password='PrintProcessing',
                              host='151.248.114.217',
                              database='PrintProcessing')
cursor = cnx.cursor()
add_temperature = ("insert into Temperature(termometer_id,insert_date,temperature,pressure,humidity) "
"values (%s,sysdate(),%s,%s,%s)")
bus.write_byte(default_i2c_hub_address, 8)
#Read data from Sensor
ps = BME280()
ps_data = ps.get_data()
time.sleep(5)
ps_data = ps.get_data()
print "Temperature1:", convert(ps_data['t'], units[temperature_field]), "°"+units[temperature_field], "Pressure:", convert(ps_data['p'], units[pressure_field]), units[pressure_field], "Humidity:", ps_data['h'], units[humidity_field]

temper1 = ('1',ps_data['t'],convert(ps_data['p'], units[pressure_field]),ps_data['h'])
cursor.execute(add_temperature,temper1)

bus.write_byte(default_i2c_hub_address, 8+1)
ps = BME280()
ps_data = ps.get_data()
time.sleep(5)
ps_data = ps.get_data()
print "Temperature2:", convert(ps_data['t'], units[temperature_field]), "°"+units[temperature_field], "Pressure:", convert(ps_data['p'], units[pressure_field]), units[pressure_field], "Humidity:", ps_data['h'], units[humidity_field]

temper2 = ('2',ps_data['t'],convert(ps_data['p'], units[pressure_field]),ps_data['h'])
cursor.execute(add_temperature,temper2)
cnx.commit()

cursor.close()
cnx.close()
"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
time.sleep(5)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # подтяжка к питанию 3,3 В
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # подтяжка к земле0 В
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_OFF) # подтяжка выключена
#signal = GPIO.input(17) # считываем сигнал GPIO 17 в переменную signal
print('11 pin On')
GPIO.output(11, True) # записываем в GPIO 11 “1” (3.3 V)
time.sleep(5)
print('11 pin Off')
GPIO.output(11, False) # записываем в GPIO 11 “0” (0 V)
print('Cleanup')
GPIO.cleanup()

resp = requests.get('http://178.46.158.29:34801/admin/get_registry')
if resp.status_code != 200:
    # This means something went wrong.
    print('{}'.format(resp.status_code))
else:
    print('{} {}'.resp.json())
"""
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))