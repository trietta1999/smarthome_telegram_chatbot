from threading import Thread
from pyA20.gpio import gpio, port
import os, time, smbus, dht11

bh1750_addr = 0x23
ONE_TIME_HIGH_RES_MODE_1 = 0x20

led_data = 0
bus = ''

dht_p = [dht11.DHT11(port.PA13), dht11.DHT11(port.PA14), dht11.DHT11(port.PD14),
	dht11.DHT11(port.PC4), dht11.DHT11(port.PC7), dht11.DHT11(port.PA2)]
# ~ congtac_p = [port.PA11, port.PA6, port.PA1, port.PA0, port.PA3, port.PC0, port.PC1, port.PC2]
chotcua_p = [port.PA7, port.PA8, port.PA9, port.PG7]
hc595_p = [port.PC3, port.PA21, port.PG8] # clk, data, latch
buzz_p = port.PG9
mq_p = port.PG6
chat_p = port.PA12

def gpio_setup():
	global bus
	
	bus = smbus.SMBus(1)
	gpio.init()
	
	for b in chotcua_p:
		gpio.setcfg(b, gpio.INPUT)
		gpio.pullup(b, gpio.PULLUP)
		
	# ~ for b in congtac_p:
		# ~ gpio.setcfg(b, gpio.INPUT)
		# ~ gpio.pullup(b, gpio.PULLUP)
		
	for p in hc595_p: gpio.setcfg(p, gpio.OUTPUT)
	gpio.output(hc595_p[2], gpio.HIGH)
		
	gpio.setcfg(buzz_p, gpio.OUTPUT)
	gpio.setcfg(mq_p, gpio.INPUT)
	gpio.setcfg(chat_p, gpio.OUTPUT)
	gpio.output(chat_p, gpio.HIGH)
	
	Thread(target = lambda: os.system("python3 ledpwm.py")).start()

def write_74hc595(pin, value):
	global led_data
	if (value): led_data |= (1 << pin)
	else: led_data &= ~(1 << pin)
	gpio.output(hc595_p[2], gpio.LOW)
	for i in range(0, 8):
		gpio.output(hc595_p[1], (led_data >> (7 - i)) & 1)
		gpio.output(hc595_p[0], gpio.HIGH)
		gpio.output(hc595_p[0], gpio.LOW)
	gpio.output(hc595_p[2], gpio.HIGH)
	
def dk_den(name, value):
	if (name == "d_pk"): write_74hc595(5, value)
	elif (name == "d_pb"): write_74hc595(4, value)
	elif (name == "d_pt"): write_74hc595(3, value)
	elif (name == "d_pn1"): write_74hc595(2, value)
	elif (name == "d_pn2"): write_74hc595(1, value)
	elif (name == "d_st"): write_74hc595(0, value)
	
def dk_den_ss(name, value):
	if (name == "ss_pn1"):
		with open("pwm_control", "w") as f:
			f.write("0\n")
			f.write(str(value * 20) + "\n")
			f.write(" " * value)
	elif (name == "ss_pn2"):
		with open("pwm_control", "w") as f:
			f.write("1\n")
			f.write(str(value * 20) + "\n")
			f.write(" " * value)
		
def gpio_read(pin, debounce = False):
	if (not gpio.input(pin)):
		if (debounce == True):
			while (not gpio.input(pin)): pass
		time.sleep(0.2)
		return False
	return True
	
def gpio_write(pin, value):
	gpio.output(pin, value)
	
def dht_read():
	dht_r = []
	for dht in dht_p: dht_r.append([dht.read().temperature, dht.read().humidity])
	return dht_r

def bh1750_read(): 
	data = bus.read_i2c_block_data(bh1750_addr, ONE_TIME_HIGH_RES_MODE_1)
	result=(data[1] + (256 * data[0])) / 1.2
	return int(result)
