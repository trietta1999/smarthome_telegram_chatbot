import os, time
from pyA20.gpio import gpio, port
from orangepwm import *

gpio.init()

size_b = 0
ss_led_p = [port.PA10, port.PA20]
ss_led = [OrangePwm(100, ss_led_p[0]), OrangePwm(100, ss_led_p[1])]

ss_led[0].start(100)
ss_led[1].start(100)
ss_led[0].changeDutyCycle(0)
ss_led[1].changeDutyCycle(0)

while (True):
	try:
		ft = os.stat("pwm_control")	
		if (ft.st_size != size_b):
			size_b = ft.st_size
			with open("pwm_control", "r") as f:
				r =  f.readlines()
				ss_led[int(r[0])].changeDutyCycle(int(r[1]))
	except: pass
	time.sleep(0.001)
