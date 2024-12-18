# from machine import Pin
# import time
# led = Pin(2, Pin.OUT)
# for i in range(100):
#     led.on()
#     time.sleep(0.5)
#     led.off()
#     time.sleep(0.5)
#     
    
# from machine import Pin, I2C
# from time import sleep
# import Bme280
# 
# # ESP32 - Pin assignment
# #i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
# # ESP8266 - Pin assignment
# i2c = I2C(scl=Pin(5), sada=Pin(4), freq=10000)
# 
# while True:
#   bme = BME280.BME280(i2c=i2c)
#   temp = bme.temperature
#   hum = bme.humidity
#   pres = bme.pressure
#   # uncomment for temperature in Fahrenheit
#   #temp = (bme.read_temperature()/100) * (9/5) + 32
#   #temp = str(round(temp, 2)) + 'F'
#   print('Temperature: ', temp)
#   print('Humidity: ', hum)
#   print('Pressure: ', pres)
# 
#   sleep(5)
#   
# from machine import I2C
# from machine import Pin
# from machine import sleep
# import mpu6050
# #i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
# i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
# mpu= mpu6050.accel(i2c)
# while True:
#  mpu.get_values()
#  print(mpu.get_values())
#  sleep(500)
 
from machine import I2C
from machine import Pin
from machine import sleep
import bme280
import mpu6050
#i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
bme = bme280.BME280(i2c=i2c)
mpu= mpu6050.accel(i2c)
while True:
  
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
  # uncomment for temperature in Fahrenheit
  #temp = (bme.read_temperature()/100) * (9/5) + 32
  #temp = str(round(temp, 2)) + 'F'
    print('Temperature: ', temp)
    print('Humidity: ', hum)
    print('Pressure: ', pres)
    mpu.get_values()
    print(mpu.get_values())

    sleep(500)
