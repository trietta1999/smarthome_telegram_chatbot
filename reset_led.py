from pyA20.gpio import gpio, port

led_data = 0
hc595_p = [port.PC3, port.PA21, port.PG8] # clk, data, latch

def gpio_setup():
	gpio.init()	
	for p in hc595_p: gpio.setcfg(p, gpio.OUTPUT)
	gpio.output(hc595_p[2], gpio.HIGH)

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
	
gpio_setup()
write_74hc595(0, 0)
