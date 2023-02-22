from threading import Thread
import os, ctypes, pyotp
import telegram_bot as tb
import chuyen_form as cf
from platform import system

# otpauth://totp/TTBot?secret=ttbotbase32triettaggauth&digits=6&issuer=PythonQR
totp = pyotp.TOTP("ttbotbase32trietta", interval=60)
totp1 = pyotp.TOTP("ttbotbase32triettaggauth")

if (system() == "Windows"):
	myappid = u""
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
	if (system() == "Windows"): os.system("cls")
	else:
		os.system("clear")
		Thread(target = lambda: os.system("python3 -m uploadserver 8001")).start()
		
	print("He thong dang khoi dong...")
	Thread(target = tb.bot_start).start()
	tb.init()
	cf.init()
