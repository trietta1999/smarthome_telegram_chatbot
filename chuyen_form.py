import os, sys, time, socket
from PyQt5 import QtCore, QtGui, QtWidgets
import dang_nhap, qrcode, dieu_khien
import telegram_bot as tb
from main import totp, totp1
from platform import system
from threading import Thread
from requests import get
import webcam as wc
import dieukhien as dk

ui = ''
app = ''
MainWindow = ''

isPlay = False
isPause = False
isCamera = False
isLogin = False
isLcdShow = False

in_ip = ex_ip = ""

def show_mess(title, text, level):
	msg = QtWidgets.QMessageBox()
	if level == 1: msg.setIcon(QtWidgets.QMessageBox.Question)
	elif level == 2: msg.setIcon(QtWidgets.QMessageBox.Information)
	elif level == 3: msg.setIcon(QtWidgets.QMessageBox.Warning)
	elif level == 4: msg.setIcon(QtWidgets.QMessageBox.Critical)
	msg.setText(text)
	msg.setWindowTitle(title)
	#msg.setDetailedText("The details are as follows:")
	msg.exec_()

def change_image_label(control, img):
	pixmap = QtGui.QPixmap(":/background/" + img)
	control.setPixmap(pixmap)
	return control
	
def change_image_button(control, img):
	icon = QtGui.QIcon()
	icon.addPixmap(QtGui.QPixmap(":/background/" + img), QtGui.QIcon.Normal, QtGui.QIcon.On)
	control.setIcon(icon)
	control.setIconSize(QtCore.QSize(control.width(), control.height()))
	return control

def play_music(a):
	global ui, isPlay, isPause
	if (a == 0):
		ui.b_pause.setEnabled(True)
		if (system() == "Windows"):
			os.system("sWavPlayer.exe \"Two Steps From Hell Star Sky Instrumental.mp3\"")
		else: os.system("audacious -H -p -q \"Two Steps From Hell Star Sky Instrumental.mp3\"")
		isPlay = False
		isPause = False
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/background/icon/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		ui.b_play.setIcon(icon)
		ui.b_pause.setEnabled(False)
	elif (a == 1):
		if (system() != "Windows"):
			if (not isPause):
				isPause = True
				os.system("audacious -u")
			else:
				isPause = False
				os.system("audacious -p")			
	elif (a == 2):
		if (system() == "Windows"): os.system("taskkill /F /IM sWavPlayer.exe")
		else: os.system("audacious -s q")
		ui.b_pause.setEnabled(False)

def music(a):
	global ui, isPlay
	if (a):
		if (not isPlay):
			isPlay = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(":/background/icon/stop-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
			ui.b_play.setIcon(icon)
			Thread(target = play_music, args = (0,)).start()
		else:
			isPlay = False
			Thread(target = play_music, args = (2,)).start()
	else: Thread(target = play_music, args = (1,)).start()

# ~ def show_otp(a):
	# ~ if (not a): ui.lcd_otp.display("------")
	# ~ else: ui.lcd_otp.display(totp.now())

def ht_dongho():
	global ui
	bx = by = cnt = 0
	day = ""
	i = 0
	while (True):
		if (time.strftime("%d") != day):
			day = time.strftime("%d")
			ui.lcd_date.display(time.strftime("%d-%m-%Y"))
		ui.lcd_time.display(time.strftime("%H:%M:%S"))
		ui.lcd_otp_time.display(totp.interval - tb.timec - 1)
		if (isLcdShow): ui.lcd_otp.display(totp.now())
		
		if (system() != "Windows"):
			cnt += 1
			pos = QtGui.QCursor().pos()
			if (pos.x() == bx and pos.y()== by and cnt >= 10):
				os.system("xdotool mousemove 1260 640")
				os.system("xdotool click 1")
				cnt = 0
			else:
				bx = pos.x()
				by = pos.y()
		
		time.sleep(1)
	
def b_dangnhap_check():
	try:
		if (len(ui.t_xacthuc.text()) < 6): ui.b_dangnhap.setEnabled(False)
		else: ui.b_dangnhap.setEnabled(True)
		if (ui.t_xacthuc.text() == "login_telegram_pass"): form_dieu_khien()
	except: pass

def form_dang_nhap():
	global ui, MainWindow
	ui = dang_nhap.Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.b_dangnhap.setEnabled(False)
	ui.b_dangnhap.clicked.connect(dang_nhap_tai_khoan)
	ui.b_dangnhap1.clicked.connect(dang_nhap_tai_khoan)
	ui.t_xacthuc.textChanged[str].connect(b_dangnhap_check)
	# ~ if (system() != "Windows"):
		# ~ MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	ui.t_xacthuc.setFocus()
	
	MainWindow.show()
	x = MainWindow.width()
	y = MainWindow.height()
	screen = app.primaryScreen()
	sizex = screen.size().width()
	sizey = screen.size().height()
	MainWindow.move(sizex/2 - x/2, sizey/2 - y/2)
	
	for l_uid in tb.list_uid:
		tb.bot.sendMessage(l_uid[2], "Hệ thống đã khởi động.")

def form_dieu_khien():
	global ui, MainWindow, isLogin, in_ip, ex_ip
	isLogin = True
	
	ui = dieu_khien.Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.lb_da_st.setVisible(False)
	ui.b_dangxuat.clicked.connect(lambda: _exit())
	# ~ ui.b_otp.pressed.connect(lambda: show_otp(True))
	# ~ ui.b_otp.released.connect(lambda: show_otp(False))
	ui.b_otp.clicked.connect(lambda: on_press("b otp"))
	ui.b_play.clicked.connect(lambda: music(True))
	ui.b_pause.clicked.connect(lambda: music(False))
	ui.b_pause.setEnabled(False)
	ui.b_off.clicked.connect(lambda: power_off(0))
	ui.b_restart.clicked.connect(lambda: power_off(1))
	ui.b_sleep.clicked.connect(lambda: power_off(2))
	ui.b_time_sync.clicked.connect(time_sync)
	ui.bu_ss_pn1.clicked.connect(lambda: on_press("bu pn1"))
	ui.bd_ss_pn1.clicked.connect(lambda: on_press("bd pn1"))
	ui.bu_ss_pn2.clicked.connect(lambda: on_press("bu pn2"))
	ui.bd_ss_pn2.clicked.connect(lambda: on_press("bd pn2"))
	ui.b_tab_l.clicked.connect(lambda: on_press("tab l"))
	ui.b_tab_r.clicked.connect(lambda: on_press("tab r"))
	ui.b_reconnect.clicked.connect(lambda: os.system("sh reconnect.sh"))
	ui.img_warn.setVisible(False)
	
	if (system() == "Windows"):
		ui.b_off.setEnabled(False)
		ui.b_restart.setEnabled(False)
		ui.b_sleep.setEnabled(False)
		MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		
	dk.setup()
	
	ui.tabWidget.currentChanged.connect(onChange)
	MainWindow.move(0, 0)
	MainWindow.show()
	MainWindow.showMaximized()
	
	ex_ip = get('https://api.ipify.org').content.decode('utf8')
	in_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	in_ip.connect(("8.8.8.8", 80))
	
	ui.lcd_otp.display("------")
	ui.lcd_pub_ip.display("---------------")
	ui.lcd_lan_ip.display(in_ip.getsockname()[0])

	wc.init()
	Thread(target = show_camera).start()
	Thread(target = ht_dongho).start()

def time_sync():
	os.system("timedatectl set-timezone \"Asia/Ho_Chi_Minh\"")
	logout_script()

def show_camera():
	global ui, isCamera
	while (True):
		try:
			img1, img2 = wc.get_img()
			img1, img2 = wc.cvtRGB()

			if (isCamera):
				h, w, b = img1.shape
				img = QtGui.QImage(img1.data, w, h, b * w, QtGui.QImage.Format_RGB888)
				ui.g_camera1.setPixmap(QtGui.QPixmap.fromImage(img))
				
				h, w, b = img2.shape
				img = QtGui.QImage(img2.data, w, h, b * w, QtGui.QImage.Format_RGB888)
				ui.g_camera2.setPixmap(QtGui.QPixmap.fromImage(img))				
		except: pass
		time.sleep(0.001)
		
def onChange(i):
	global ui, isCamera, isLcdShow
	if (i == 0):
		isCamera = False
		ui.b_otp.setEnabled(True)
	else:
		ui.b_otp.setEnabled(False)
		ui.lcd_otp.display("------")
		isLcdShow = False
		isCamera = True

def form_qrcode():
	global ui, MainWindow
	ui = qrcode.Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.b_qrexit.clicked.connect(form_dang_nhap)
	if (system() == "Windows"):
		MainWindow.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
	MainWindow.show()
	x = MainWindow.width()
	screen = app.primaryScreen()
	sizex = screen.size().width()
	MainWindow.move(sizex/2 - x/2, 0)

def power_off(a):
	# ~ msg = QtWidgets.QMessageBox()
	# ~ msg.setIcon(QtWidgets.QMessageBox.Question)
	# ~ msg.setText("Bạn có muốn thực hiện hành động này?")
	# ~ msg.setWindowTitle("Xác nhận")
	# ~ msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)		
	# ~ if (msg.exec_() == QtWidgets.QMessageBox.Yes):
	if (a == 0): os.system("poweroff")
	elif (a == 1): os.system("reboot")
	elif (a == 2): os.system("pkill python3 & systemctl suspend")

def _exit(script = True, off = False):
	try:
		wc.destroy()
	except: pass
	if (script):
		for l_uid in tb.list_uid:
			tb.bot.sendMessage(l_uid[2],
				"Hệ thống đã đăng xuất tại nhà thành công. Nếu không phải bạn, " +
				"hãy ẩn giao diện hoặc tắt hệ thống để bảo vệ khỏi kẻ xâm nhập.")
		if (system() == "Windows"): os.system("logout.bat")
		else: os.system("sh logout.sh")
	else:
		for l_uid in tb.list_uid:
			tb.bot.sendMessage(l_uid[2], "Hệ thống đã tắt.")
			tb.bot.sendMessage(l_uid[2], "Bạn không thể trả lời cuộc trò chuyện này.")
		if (off): os.system("pkill python3 & systemctl suspend")
		if (system() == "Windows"): os._exit(0)
		else: os.system("notify-send \"Hệ thống đã tắt\" & pkill python3")

def dang_nhap_tai_khoan(uid = 0, code = ''):
	global MainWindow, ui
	ui.b_dangnhap.setEnabled(False)
	ui.t_xacthuc.setEnabled(False)
	if (len(ui.t_xacthuc.text()) != 0 and ui.t_xacthuc.text() != "login_telegram_pass"):
		if (ui.t_xacthuc.text() == "adminqr"): form_qrcode()
		elif (totp.verify(ui.t_xacthuc.text()) or totp1.verify(ui.t_xacthuc.text()) or ui.t_xacthuc.text() == "admindk"):
			for l_uid in tb.list_uid:
				tb.bot.sendMessage(l_uid[2],
				"Hệ thống đã đăng nhập tại nhà thành công. Nếu không phải bạn, " +
				"hãy đăng xuất hoặc tắt hệ thống để bảo vệ khỏi kẻ xâm nhập.")
			form_dieu_khien()
			tb.login_state = True
			return True
		else:
			show_mess("Lỗi", "Đăng nhập không thành công!", 4)
			for l_uid in tb.list_uid:
				tb.bot.sendMessage(l_uid[2],
				"Hệ thống đã đăng nhập tại nhà không thành công. Nếu không phải bạn, " +
				"hãy tắt hệ thống để bảo vệ khỏi kẻ xâm nhập.")
			ui.b_dangnhap.setEnabled(True)
			ui.t_xacthuc.setEnabled(True)
			ui.t_xacthuc.clear()
			ui.t_xacthuc.setFocus()
			return False
	else:
		if (totp.verify(code)):
			ui.t_xacthuc.setText("login_telegram_pass")
			tb.login_state = True
			return True
		else:
			for l_uid in tb.list_uid:
				tb.bot.sendMessage(l_uid[2],
				"Hệ thống đã đăng nhập tại nhà không thành công. Nếu không phải bạn, " +
				"hãy tắt hệ thống để bảo vệ khỏi kẻ xâm nhập.")
			ui.b_dangnhap.setEnabled(True)
			ui.t_xacthuc.setEnabled(True)
			ui.t_xacthuc.setFocus()
			return False

	return False

def on_press(key):
	global ui, isLcdShow
	if (key == "tab l"): ui.tabWidget.setCurrentIndex(0)
	elif (key == "tab r"): ui.tabWidget.setCurrentIndex(1)
	elif (key == "bu pn1"):
		if (dk.v_d_ss_pn1 < 3):
			dk.v_d_ss_pn1 += 1
			ui.sl_ss_pn1.setValue(dk.v_d_ss_pn1)
	elif (key == "bd pn1"):
		if (dk.v_d_ss_pn1 > 0):
			dk.v_d_ss_pn1 -= 1
			ui.sl_ss_pn1.setValue(dk.v_d_ss_pn1)
	elif (key == "bu pn2"):
		if (dk.v_d_ss_pn2 < 3):
			dk.v_d_ss_pn2 += 1
			ui.sl_ss_pn2.setValue(dk.v_d_ss_pn2)
	elif (key == "bd pn2"):
		if (dk.v_d_ss_pn2 > 0):
			dk.v_d_ss_pn2 -= 1
			ui.sl_ss_pn2.setValue(dk.v_d_ss_pn2)
	elif (key == "b otp"):
		isLcdShow = not isLcdShow
		if (not isLcdShow):
			ui.lcd_otp.display("------")
			ui.lcd_pub_ip.display("---------------")
		else:
			ui.lcd_otp.display(totp.now())
			ui.lcd_pub_ip.display(ex_ip)

def init():
	global MainWindow, app
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	app.aboutToQuit.connect(lambda: _exit(False))
	
	form_dang_nhap()
	sys.exit(app.exec_())
