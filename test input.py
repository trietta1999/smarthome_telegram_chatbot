from pyA20.gpio import gpio, port
from time import sleep
from os import system
from threading import Thread

congtac_p = [port.PA11, port.PA6, port.PA1, port.PA0, port.PA3, port.PC0, port.PC1, port.PC2]
chotcua_p = [port.PA7, port.PA8, port.PA9, port.PG7, port.PG6]

def gpio_setup():
	gpio.init()
	
	for b in chotcua_p:
		gpio.setcfg(b, gpio.INPUT)
		# ~ gpio.pullup(b, gpio.PULLUP)
		
	for b in congtac_p:
		gpio.setcfg(b, gpio.INPUT)
		gpio.pullup(b, gpio.PULLUP)
		
	gpio.setcfg(port.PG6, gpio.INPUT)

def gpio_read(pin, debounce = False):
	if (not gpio.input(pin)):
		if (debounce == True):
			while (not gpio.input(pin)): pass
		return False
	return True

door_open_list = [False, False, False, False]

gpio_setup()

def run():
	while (True):
		for b, open_d in zip(chotcua_p, door_open_list):
			current = gpio_read(b)
			if (current == True and open_d == False):
				door_open_list[chotcua_p.index(b)] = True
				print(chotcua_p.index(b), "open")
			elif (current == False and open_d == True):
				door_open_list[chotcua_p.index(b)] = False
				print(chotcua_p.index(b), "close")
		print(door_open_list, gpio_read(port.PG6))
		
		# ~ for b in congtac_p:
			# ~ print(congtac_p.index(b), gpio_read(b))
		
		sleep(0.01)
		system("clear")
		
th = Thread(target=run)
th.start()
