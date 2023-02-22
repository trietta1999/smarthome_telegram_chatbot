import time, os
import chuyen_form as cf
from platform import system
from threading import Thread

door_open_list = [False, False, False, False]
s_d_pk = s_d_pb = s_d_pt = s_d_pn1 = s_d_pn2 = s_d_st = False
isDone = mq_on = False
v_d_ss_pn1 = v_d_ss_pn2 = 0
command = ""

if (system() == "Windows"):
	from gpiopy_win import *
	
	def h_input():
		global command, isDone
		while (True):
			command = input("Code: ")
			if (command == "exit"): break
			isDone = False
			while (isDone == False): pass
			command = ""
		os._exit(0)

	Thread(target = h_input).start()
	
else: from gpiopy import *

def setup():
	cf.ui.sw_d_pk.clicked.connect(h_d_pk)
	cf.ui.sw_d_pb.clicked.connect(h_d_pb)
	cf.ui.sw_d_pt.clicked.connect(h_d_pt)
	cf.ui.sw_d_pn1.clicked.connect(h_d_pn1)
	cf.ui.sw_d_pn2.clicked.connect(h_d_pn2)
	cf.ui.sw_d_st.clicked.connect(h_d_st)
	
	cf.ui.sl_ss_pn1.valueChanged.connect(h_ss_pn1)
	cf.ui.sl_ss_pn2.valueChanged.connect(h_ss_pn2)
	
	gpio_setup()
	
	Thread(target = ht_thongtin).start()
	Thread(target = h_dk_den).start()
	
def h_d_pk():
	global s_d_pk
	s_d_pk = not s_d_pk
	if (s_d_pk):
		cf.ui.img_d_pk = cf.change_image_label(cf.ui.img_d_pk, "icon/lamp.png")
		cf.ui.sw_d_pk = cf.change_image_button(cf.ui.sw_d_pk, "icon/swh_on.png")		
		dk_den("d_pk", True)
		return True
	else:
		cf.ui.img_d_pk = cf.change_image_label(cf.ui.img_d_pk, "icon/lamp_off.png")
		cf.ui.sw_d_pk = cf.change_image_button(cf.ui.sw_d_pk, "icon/swh_off.png")	
		dk_den("d_pk", False)
		return False
		
def h_d_pb():
	global s_d_pb
	s_d_pb = not s_d_pb
	if (s_d_pb):
		cf.ui.img_d_pb = cf.change_image_label(cf.ui.img_d_pb, "icon/lamp.png")
		cf.ui.sw_d_pb = cf.change_image_button(cf.ui.sw_d_pb, "icon/swh_on.png")
		dk_den("d_pb", True)
		return True
	else:
		cf.ui.img_d_pb = cf.change_image_label(cf.ui.img_d_pb, "icon/lamp_off.png")
		cf.ui.sw_d_pb = cf.change_image_button(cf.ui.sw_d_pb, "icon/swh_off.png")
		dk_den("d_pb", False)
		return False
		
def h_d_pt():
	global s_d_pt
	s_d_pt = not s_d_pt
	if (s_d_pt):
		cf.ui.img_d_pt = cf.change_image_label(cf.ui.img_d_pt, "icon/lamp.png")
		cf.ui.sw_d_pt = cf.change_image_button(cf.ui.sw_d_pt, "icon/swh_on.png")
		dk_den("d_pt", True)
		return True
	else:
		cf.ui.img_d_pt = cf.change_image_label(cf.ui.img_d_pt, "icon/lamp_off.png")
		cf.ui.sw_d_pt = cf.change_image_button(cf.ui.sw_d_pt, "icon/swh_off.png")
		dk_den("d_pt", False)
		return False

def h_d_pn1():
	global s_d_pn1
	s_d_pn1 = not s_d_pn1
	if (s_d_pn1):
		cf.ui.img_d_pn1 = cf.change_image_label(cf.ui.img_d_pn1, "icon/lamp.png")
		cf.ui.sw_d_pn1 = cf.change_image_button(cf.ui.sw_d_pn1, "icon/sw_on.png")
		dk_den("d_pn1", True)
		return True
	else:
		cf.ui.img_d_pn1 = cf.change_image_label(cf.ui.img_d_pn1, "icon/lamp_off.png")
		cf.ui.sw_d_pn1 = cf.change_image_button(cf.ui.sw_d_pn1, "icon/sw_off.png")
		dk_den("d_pn1", False)
		return False
		
def h_d_pn2():
	global s_d_pn2
	s_d_pn2 = not s_d_pn2
	if (s_d_pn2):
		cf.ui.img_d_pn2 = cf.change_image_label(cf.ui.img_d_pn2, "icon/lamp.png")
		cf.ui.sw_d_pn2 = cf.change_image_button(cf.ui.sw_d_pn2, "icon/sw_on.png")
		dk_den("d_pn2", True)
		return True
	else:
		cf.ui.img_d_pn2 = cf.change_image_label(cf.ui.img_d_pn2, "icon/lamp_off.png")
		cf.ui.sw_d_pn2 = cf.change_image_button(cf.ui.sw_d_pn2, "icon/sw_off.png")
		dk_den("d_pn2", False)
		return False
		
def h_d_st():
	global s_d_st
	s_d_st = not s_d_st
	if (s_d_st):
		cf.ui.img_d_st = cf.change_image_label(cf.ui.img_d_st, "icon/lamp.png")
		cf.ui.sw_d_st = cf.change_image_button(cf.ui.sw_d_st, "icon/sw_on.png")
		dk_den("d_st", True)
		return True
	else:
		cf.ui.img_d_st = cf.change_image_label(cf.ui.img_d_st, "icon/lamp_off.png")
		cf.ui.sw_d_st = cf.change_image_button(cf.ui.sw_d_st, "icon/sw_off.png")
		dk_den("d_st", False)
		return False
		
def h_ss_pn1(value = -1):
	global v_d_ss_pn1
	
	if (value == -1): v_d_ss_pn1 = cf.ui.sl_ss_pn1.value()
	else: v_d_ss_pn1 = value
	
	if (v_d_ss_pn1 == 0):
		cf.ui.img_ss_pn1 = cf.change_image_label(cf.ui.img_ss_pn1, "icon/lamp_off.png")
	elif (v_d_ss_pn1 > 0 and v_d_ss_pn1 < 3):
		cf.ui.img_ss_pn1 = cf.change_image_label(cf.ui.img_ss_pn1, "icon/lamp%d.png" % v_d_ss_pn1)
	else:
		cf.ui.img_ss_pn1 = cf.change_image_label(cf.ui.img_ss_pn1, "icon/lamp.png")	
	dk_den_ss("ss_pn1", v_d_ss_pn1)
	
def h_ss_pn2(value = -1):
	global v_d_ss_pn2
	if (value == -1): v_d_ss_pn2 = cf.ui.sl_ss_pn2.value()
	else: v_d_ss_pn2 = value
	if (v_d_ss_pn2 == 0):
		cf.ui.img_ss_pn2 = cf.change_image_label(cf.ui.img_ss_pn2, "icon/lamp_off.png")
	elif (v_d_ss_pn2 > 0 and v_d_ss_pn2 < 3):
		cf.ui.img_ss_pn2 = cf.change_image_label(cf.ui.img_ss_pn2, "icon/lamp%d.png" % v_d_ss_pn2)
	else:
		cf.ui.img_ss_pn2 = cf.change_image_label(cf.ui.img_ss_pn2, "icon/lamp.png")
	dk_den_ss("ss_pn2", v_d_ss_pn2)

def open_door():
	gpio_write(chat_p, False)
	time.sleep(0.5)
	gpio_write(chat_p, True)

def read_door():
	return gpio_read(chotcua_p[3])

def ht_thongtin():
	global command, isDone, door_open_list, mq_on
	
	label_l = [[cf.ui.lb_nd_pk, cf.ui.lb_da_pk], [cf.ui.lb_nd_pb, cf.ui.lb_da_pb],
		[cf.ui.lb_nd_pt, cf.ui.lb_da_pt], [cf.ui.lb_nd_pn1, cf.ui.lb_da_pn1], 
		[cf.ui.lb_nd_pn2, cf.ui.lb_da_pn2], [cf.ui.lb_nd_st, cf.ui.lb_da_st]]
	door_l = [cf.ui.img_c_pt, cf.ui.img_c_pn1, cf.ui.img_c_pn2, cf.ui.img_c_st]
		
	dht_value_list = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
	mq_on = False
	time_b = 0
	
	while (True):
		if (time.time() - time_b >= 0.5):
			time_b = time.time()
			dht_r = dht_read()
			for label, dht in zip(label_l, dht_r):
				if (dht[0] != 0 and dht[1] != 0):
					label[0].setText(str(dht[0]))
					label[1].setText(str(dht[1]))
			cf.ui.lb_as_st.setText(str(bh1750_read()))		
		if (system() == "Windows"):
			if (command == "mq on"):
				cf.ui.img_mq = cf.change_image_label(cf.ui.img_mq, "icon/smoke_detector_on.png")
				cf.ui.img_warn.setVisible(True)
				mq_on = True
				isDone = True
			elif (command == "mq off"):
				cf.ui.img_mq = cf.change_image_label(cf.ui.img_mq, "icon/smoke_detector.png")
				cf.ui.img_warn.setVisible(False)
				mq_on = False
				isDone = True
			elif ("door" in command):
				c = command.split(' ')
				if (c[2] == "open"):
					door_l[int(c[1])] = cf.change_image_label(door_l[int(c[1])], "icon/door_open.png")
					door_open_list[int(c[1]) - 1] = True
				else:
					door_l[int(c[1])] = cf.change_image_label(door_l[int(c[1])], "icon/door.png")
					door_open_list[int(c[1])] = False
				isDone = True
			elif (command == "list uid"):
				print(tb.list_uid)
				isDone = True
			elif ("tab" in command):
				c = command.split(' ')
				cf.ui.tabWidget.setCurrentIndex(int(c[1]))
				isDone = True
		else:
			mq_r = gpio_read(mq_p)
			if (mq_r == False and mq_on == False):
				mq_on = True
				cf.ui.img_mq = cf.change_image_label(cf.ui.img_mq, "icon/smoke_detector_on.png")
				cf.ui.img_warn.setVisible(True)
				gpio_write(buzz_p, True)
			elif (mq_r == True and mq_on == True):
				mq_on = False
				cf.ui.img_mq = cf.change_image_label(cf.ui.img_mq, "icon/smoke_detector.png")
				cf.ui.img_warn.setVisible(False)
				gpio_write(buzz_p, False)
			# ~ for b, open_d in zip(chotcua_p, door_open_list):
				# ~ current = gpio_read(b)
				# ~ index = chotcua_p.index(b) 
				# ~ if (current == True and open_d == False):
					# ~ door_open_list[index] = True
					# ~ door_l[index] = cf.change_image_label(door_l[index], "icon/door_open.png")
				# ~ elif (current == False and open_d == True):
					# ~ door_open_list[index] = False
					# ~ door_l[index] = cf.change_image_label(door_l[index], "icon/door.png")
			door = gpio_read(chotcua_p[3])
			if (door == True and door_open_list[3] == False):
				door_open_list[3] = True
				door_l[3] = cf.change_image_label(door_l[3], "icon/door_open.png")
			elif (door == False and door_open_list[3] == True):
				door_open_list[3] = False
				door_l[3] = cf.change_image_label(door_l[3], "icon/door.png")
							
		time.sleep(0.001)

def dk_den_callback(button_s, callback, win = False):
	if (not win):
		if (not button_s): callback()
	else:
		if (button_s): callback()
	return True

def h_dk_den():
	global command, isDone, v_d_ss_pn1, v_d_ss_pn2
	
	while (True):
		if (system() == "Windows"):		
			isDone = dk_den_callback(command == "ct d 0", h_d_pk, True)
			isDone = dk_den_callback(command == "ct d 1", h_d_pb, True)
			isDone = dk_den_callback(command == "ct d 2", h_d_pt, True)
			isDone = dk_den_callback(command == "ct d 3", h_d_pn1, True)
			isDone = dk_den_callback(command == "ct d 4", h_d_pn2, True)
			isDone = dk_den_callback(command == "ct d 5", h_d_st, True)
			
			if (command == "ct d ss 0"):
				v_d_ss_pn1 += 1
				if (v_d_ss_pn1 == 4): v_d_ss_pn1 = 0
				h_ss_pn1(v_d_ss_pn1)
				cf.ui.sl_ss_pn1.setValue(v_d_ss_pn1)
				isDone = True
			elif (command == "ct d ss 1"):
				v_d_ss_pn2 += 1
				if (v_d_ss_pn2 == 4): v_d_ss_pn2 = 0
				h_ss_pn2(v_d_ss_pn2)
				cf.ui.sl_ss_pn2.setValue(v_d_ss_pn2)
				isDone = True
		else:
			dk_den_callback(gpio_read(congtac_p[0], True), h_d_pk)
			dk_den_callback(gpio_read(congtac_p[1], True), h_d_pb)
			dk_den_callback(gpio_read(congtac_p[2], True), h_d_pt)
			dk_den_callback(gpio_read(congtac_p[3], True), h_d_pn1)
			dk_den_callback(gpio_read(congtac_p[4], True), h_d_pn2)
			dk_den_callback(gpio_read(congtac_p[5], True), h_d_st)
			
			if (not gpio_read(congtac_p[6], True)):
				v_d_ss_pn1 += 1
				if (v_d_ss_pn1 == 4): v_d_ss_pn1 = 0
				h_ss_pn1(v_d_ss_pn1)	
				cf.ui.sl_ss_pn1.setValue(v_d_ss_pn1)				
			if (not gpio_read(congtac_p[7], True)):
				v_d_ss_pn2 += 1
				if (v_d_ss_pn2 == 4): v_d_ss_pn2 = 0
				h_ss_pn2(v_d_ss_pn2)
				cf.ui.sl_ss_pn2.setValue(v_d_ss_pn2)
												
		time.sleep(0.001)
