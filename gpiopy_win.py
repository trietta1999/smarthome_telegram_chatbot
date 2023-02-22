import random

chat_p = 0

def gpio_setup(): pass
	
def gpio_end(): pass

def dk_den(name, value): pass
	
def dk_den_ss(name, value): pass
	
def gpio_read(pin): return 0

def gpio_write(pin, value): pass
	
def dht_read():
	dht_r = []
	for i in range(0, 6): dht_r.append([random.randint(28, 30), random.randint(70, 72)])
	return dht_r
	
def bh1750_read():
	return random.randint(280, 300)
