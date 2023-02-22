import os, telepot, time, socket
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import chuyen_form as cf
from platform import system
from threading import Thread
from requests import get
from main import totp
import dieukhien as dk

timec = 0

bot = telepot.Bot("5005632795:AAFph_LGZmvTJSdATmCDPIyWf75eCy_zwes")
updater = Updater("5005632795:AAFph_LGZmvTJSdATmCDPIyWf75eCy_zwes")

room_list = ["Phòng khách", "Phòng bếp", "Phòng tắm", "Phòng ngủ 1", "Phòng ngủ 2", "Sân trước"]
h_d_list = [[dk.h_d_pk, "Đèn phòng khách"], [dk.h_d_pb, "Đèn phòng bếp"],
			[dk.h_d_pt, "Đèn phòng tắm"], [dk.h_d_pn1, "Đèn phòng ngủ 1"],
			[dk.h_d_pn2, "Đèn phòng ngủ 2"], [dk.h_d_st, "Đèn sân trước"]]
h_ss_list = [[dk.h_ss_pn1, "Độ sáng đèn phòng ngủ 1:"],
			[dk.h_ss_pn2, "Độ sáng đèn phòng ngủ 2:"]]

turnoff_state = False
hide_state = False
login_state = False
in_cmd_quest = False
list_uid = []

def text_find(text, str_list):
	for str0 in str_list:
		if (text.find(str0) >= 0): return True
	return False

def check_uid(c_uid):
	for user in list_uid:
		if (c_uid == user[2]): return True
	return False

def start(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	update.message.reply_markdown_v2("Xin chào " + user.mention_markdown_v2() +
		", bạn có yêu cầu gì không?")

def end(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	update.message.reply_markdown_v2("Tạm biệt " + user.mention_markdown_v2() +
		", hãy nhắn tin cho tôi nếu bạn muốn giúp đỡ\.")

def bot_command(update: Update, context: CallbackContext) -> None:
	global code, in_cmd_quest, list_uid, turnoff_state, hide_state, login_state
	command = ''
	command = list(map(lambda x: x.lower(), context.args))
	if (check_uid(update.message.chat.id)) == True:
		if (in_cmd_quest == False):
			if (len(command) != 0):
				if (command[0] == "xacthuc"):
					update.message.reply_text(totp.now())
					update.message.reply_text("Thời gian còn lại: %d giây" % (totp.interval - timec - 1))
				elif (command[0] == "taikhoan"):
					if (len(command) < 2): update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						sum0 = 0
						for tk in enumerate(list_uid):
							update.message.reply_text(
								str(tk[0]) + ". Tên: " + tk[1][0] + " " +
								tk[1][1] + "\n    UID: " + str(tk[1][2]))
							sum0 += 1
						update.message.reply_text("Tổng tài khoản người dùng: " + str(sum0))
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				elif (command[0] == "dangnhap" and login_state == False):
					if (len(command) < 2): update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					else:
						user = update.effective_user
						if (cf.dang_nhap_tai_khoan(code=command[1])):
							update.message.reply_markdown_v2(
								"Hệ thống đăng nhập từ xa thành công bởi " + user.mention_markdown_v2() +
								"\. Nếu không phải bạn, hãy đăng xuất hoặc tắt hệ thống để bảo vệ khỏi kẻ xâm nhập\.")
							login_state = True
						else:
							update.message.reply_markdown_v2(
								"Hệ thống đăng nhập từ xa không thành công bởi " + user.mention_markdown_v2() +
								"\. Nếu nghi ngờ xâm nhập, hãy đăng xuất hoặc tắt hệ thống để bảo vệ khỏi kẻ xâm nhập\.")
				elif (command[0] == "dangnhap" and login_state == True):
					update.message.reply_text("Hệ thống đã được đăng nhập.")				
				elif (command[0] == "dangxuat" and login_state == True):
					if (len(command) < 2): update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					else:
						user = update.effective_user
						if (totp.verify(command[1])):
							update.message.reply_markdown_v2(
								"Hệ thống đăng xuất từ xa thành công bởi " + user.mention_markdown_v2() +
								"\. Nếu không phải bạn, hãy tắt hệ thống để bảo vệ khỏi kẻ xâm nhập\.")
							login_state = False
							if (system() == "Windows"): os.system("logout.bat")
							else: os.system("sh logout.sh")
						else:
							update.message.reply_markdown_v2(
								"Hệ thống đăng xuất từ xa không thành công bởi " + user.mention_markdown_v2() +
								"\. Nếu nghi ngờ xâm nhập, hãy đăng xuất hoặc tắt hệ thống để bảo vệ khỏi kẻ xâm nhập\.")
				elif (command[0] == "dangxuat" and login_state == False):
					update.message.reply_text("Hệ thống đã được đăng xuất.")				
				elif (command[0] == "xoataikhoan"):
					if (len(command) < 3): update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					else:
						try:
							uid = list_uid[int(command[1])][2]
							if (totp.verify(command[2])):					
								list_uid.remove(list_uid[int(command[1])])
								update.message.reply_text("Xóa tài khoản " + str(uid) + " thành công")
								f = open("data.txt", "w")
								for uid in list_uid:
									f.writelines(uid[0] + "," + uid[1] + "," + str(uid[2])+ ",\n")
								f.close()
							else:
								update.message.reply_text("Xóa tài khoản " + str(uid) +
									" không thành công. Hãy kiểm tra lại thông tin và mã xác thực.")
						except: update.message.reply_text("Tài khoản không tồn tại.")
				elif (command[0] == "tathethong"):
					if (len(command) < 2): update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						update.message.reply_text(
							"Trong trường hợp nghi ngờ xâm nhập trái phép và KHẨN CẤP. " +
							"Nếu tắt hệ thống, bạn sẽ không thể đăng nhập hoặc khởi động từ xa, " +
							"nhập \"y\" để xác nhận tắt hoặc \"n\" để hủy bỏ.")
						turnoff_state = True
						in_cmd_quest = True
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				elif (command[0] == "anhethong"):
					if len(command) < 2: update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						update.message.reply_text(
							"Trong trường hợp nghi ngờ xâm nhập trái phép và KHÔNG khẩn cấp, " +
							"bạn có thể ẩn giao diện hệ thống để tránh sự tò mò, khi đó bạn vẫn " +
							"có thể điều khiển được mọi thiết bị trong nhà và giám sát từ xa, " +
							"nhập \"y\" để xác nhận ẩn hoặc \"n\" để hủy bỏ.")
						hide_state = True
						in_cmd_quest = True
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				elif (command[0] == "hienhethong"):
					if len(command) < 2: update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						update.message.reply_text("Đã khôi phục giao diện hệ thống.")
						cf.MainWindow.show()
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				elif (command[0] == "qrcode"):
					if (totp.verify(command[1])):
						update.message.reply_text("Đang gửi mã QR...")
						update.message.reply_photo(photo=open("image/qr.png", "rb"))
				elif (command[0] == "layip"):
					if len(command) < 2: update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						update.message.reply_text("Đang lấy địa chỉ mạng...")
						ex_ip = get('https://api.ipify.org').content.decode('utf8')
						in_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						in_ip.connect(("8.8.8.8", 80))
						update.message.reply_text("Địa chỉ camera:\nPUB IP: http://%s:8000\nLAN IP: http://%s:8000"
							% (ex_ip, in_ip.getsockname()[0]))
						update.message.reply_text("Địa chỉ file server:\nLAN IP: http://%s:8001" % in_ip.getsockname()[0])
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				elif (command[0] == "wifi"):
					if len(command) < 2: update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
					elif (totp.verify(command[1])):
						update.message.reply_text("Đang ngắt kết nối WiFi...")
						os.system("sh reconnect.sh")
						update.message.reply_text("Đã kết nối WiFi thành công.")
					else: update.message.reply_text("Mã xác thực chưa đúng.")
				else: update.message.reply_text("Lệnh không đúng.")
			else:
				update.message.reply_text(
					"Danh sách các lệnh cần ghi nhớ để sử dụng toàn bộ tính năng của hệ thống.\
					\n\n/admin xacthuc - Lấy mã xác thực OTP \
					\n/admin taikhoan <mã Authenticator> - Hiển thị danh sách tài khoản người dùng đã đăng ký\
					\n/admin dangnhap <mã Authenticator> - Đăng nhập hệ thống từ xa\
					\n/admin dangxuat <mã Authenticator> - Đăng xuất hệ thống từ xa\
					\n/admin xoataikhoan <số thứ tự> <mã Authenticator> - Xóa tài khoản người dùng\
					\n/admin tathethong <mã Authenticator> - Tắt hệ thống từ xa\
					\n/admin anhethong <mã Authenticator> - Ẩn giao diện hệ thống từ xa\
					\n/admin hienhethong <mã Authenticator> - Hiển thị giao diện hệ thống từ xa\
					\n/admin qrcode <mã Authenticator> - Hiển thị mã QR Code (sử dụng đăng nhập tại nhà và đăng ký tài khoản)\
					\n/admin layip <mã Authenticator> - Lấy địa chỉ mạng\
					\n/admin wifi <mã Authenticator> - Khởi động lại kết nối WiFi (sử dụng khi WebServer mất kết nối)\
				")
		else: update.message.reply_text("Lệnh hiện tại không khả dụng.")
	elif (check_uid(update.message.chat.id) == False):
		if (len(command) != 0):
			if (command[0] == "dangky" and len(command) < 2):
				update.message.reply_text("Lệnh chưa đầy đủ thông tin.")
			elif (command[0] == "dangky"):
				if (totp.verify(command[1])):
					update.message.reply_text(
						"Cám ơn bạn đã đăng ký, bây giờ bạn có thể sử dụng toàn bộ tính năng của hệ thống.")
					list_uid.append([update.message.chat.first_name, update.message.chat.last_name,
						update.message.chat.id])
					f = open("data.txt", "a")
					f.writelines(list_uid[-1][0] + "," + list_uid[-1][1] + "," + str(list_uid[-1][2])+ ",\n")
					f.close()
				else: update.message.reply_text("Mã xác thực không đúng.")
			else: update.message.reply_text("Lệnh không đúng.")
		else:
			update.message.reply_text(
				"Tài khoản của bạn chưa được đăng ký, do đó không thể sử dụng toàn bộ tính năng " +
				"của hệ thống, hãy sử dụng lệnh sau nếu bạn quyết định đăng ký để được cấp quyền đầy đủ.\
				\n\n/admin dangky <mã Authenticator>\
			")

def bot_control(update: Update, context: CallbackContext) -> None:
	if (cf.isLogin):
		if (check_uid(update.message.chat.id) == True):
			if (in_cmd_quest == False):
				keyboard0 = [
					[InlineKeyboardButton("Mở khóa cửa trước", callback_data = 6)],
					[InlineKeyboardButton("Bật/Tắt đèn phòng khách", callback_data = 0)],
					[InlineKeyboardButton("Bật/Tắt đèn phòng bếp", callback_data = 1)],
					[InlineKeyboardButton("Bật/Tắt đèn phòng tắm", callback_data = 2)],
					[InlineKeyboardButton("Bật/Tắt đèn phòng ngủ 1", callback_data = 3)],
					[InlineKeyboardButton("Bật/Tắt đèn phòng ngủ 2", callback_data = 4)],
					[InlineKeyboardButton("Bật/Tắt đèn sân trước", callback_data = 5)]
				]
				reply_markup = InlineKeyboardMarkup(keyboard0)
				update.message.reply_text("Bật/Tắt đèn các phòng", reply_markup=reply_markup)
				
				keyboard = [
					[
						InlineKeyboardButton("PN1 0", callback_data = 10),
						InlineKeyboardButton("PN1 1", callback_data = 11),
						InlineKeyboardButton("PN1 2", callback_data = 12),
						InlineKeyboardButton("PN1 3", callback_data = 13)
					],
					[
						InlineKeyboardButton("PN2 0", callback_data = 20),
						InlineKeyboardButton("PN2 1", callback_data = 21),
						InlineKeyboardButton("PN2 2", callback_data = 22),
						InlineKeyboardButton("PN2 3", callback_data = 23)
					]
				]
				reply_markup = InlineKeyboardMarkup(keyboard)
				update.message.reply_text("Điều chỉnh độ sáng đèn của 2 phòng ngủ", reply_markup=reply_markup)
			else: update.message.reply_text("Lệnh hiện tại không khả dụng.")
		else: update.message.reply_text("Bạn không có quyền sử dụng lệnh này, hãy sử dụng lệnh /admin.")
	else: update.message.reply_text("Hệ thống chưa đăng nhập.")
	
def bot_info(update: Update, context: CallbackContext) -> None:
	if (cf.isLogin):
		if (check_uid(update.message.chat.id) == True):
			if (in_cmd_quest == False):
				keyboard0 = [
					[
						InlineKeyboardButton("Phòng khách", callback_data = 30),
						InlineKeyboardButton("Phòng bếp", callback_data = 31)
					],
					[
						InlineKeyboardButton("Phòng tắm", callback_data = 32),
						InlineKeyboardButton("Phòng ngủ 1", callback_data = 33)
					],
					[
						InlineKeyboardButton("Phòng ngủ 2", callback_data = 34),
						InlineKeyboardButton("Khác", callback_data = 35)
					]
				]
				reply_markup = InlineKeyboardMarkup(keyboard0)
				update.message.reply_text("Chọn phòng:", reply_markup=reply_markup)
			else: update.message.reply_text("Lệnh hiện tại không khả dụng.")
		else: update.message.reply_text("Bạn không có quyền sử dụng lệnh này, hãy sử dụng lệnh /admin.")
	else: update.message.reply_text("Hệ thống chưa đăng nhập.")

def wait_door():
	while (not dk.read_door()): pass
	while (dk.read_door()): pass
	cf.ui.img_c_st_key.setVisible(True)
	for l_uid in list_uid: bot.sendMessage(l_uid[2], "Cửa trước đã khóa.")

def button(update: Update, context: CallbackContext) -> None:
	label_l = [[cf.ui.lb_nd_pk, cf.ui.lb_da_pk], [cf.ui.lb_nd_pb, cf.ui.lb_da_pb], 
		[cf.ui.lb_nd_pt, cf.ui.lb_da_pt], [cf.ui.lb_nd_pn1, cf.ui.lb_da_pn1], 
		[cf.ui.lb_nd_pn2, cf.ui.lb_da_pn2], [cf.ui.lb_nd_st, cf.ui.lb_da_st]]
	door_l = [cf.ui.img_c_pt, cf.ui.img_c_pn1, cf.ui.img_c_pn2, cf.ui.img_c_st]
	sl_list = [cf.ui.sl_ss_pn1, cf.ui.sl_ss_pn2]
	
	query = update.callback_query
	query.answer()
	num = int(query.data) % 10

	if (int(query.data) == 6):
		if (not cf.ui.img_c_st_key.isVisible()):
			query.edit_message_text(text = "Cửa trước đã mở khóa rồi.")
		else:
			dk.open_door()
			cf.ui.img_c_st_key.setVisible(False)
			Thread(target = wait_door).start()
			query.edit_message_text(text = "Cửa trước đã mở khóa.")		
	elif (int(query.data) < 10):
		r = h_d_list[int(query.data)][0]()
		query.edit_message_text(text = "%s %s" % (h_d_list[int(query.data)][1],
			"đã bật." if (r == True) else "đã tắt."))
	elif (int(query.data) >= 10 and int(query.data) < 30):
		h_ss_list[int(int(query.data) / 10) - 1][0](num)
		sl_list[int(int(query.data) / 10) - 1].setValue(num)
		query.edit_message_text(text = "%s %s" % (h_ss_list[int(int(query.data) / 10 - 1)][1], num))	
	else:
		mess = ""
		if (num == 0):
			mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s"\
			% ("Phòng khách", cf.ui.lb_nd_pk.text(), cf.ui.lb_da_pk.text(),
			"Bật" if (dk.s_d_pk == True) else "Tắt")
		elif (num == 1):
			mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nBáo động: %s"\
			% ("Phòng bếp", cf.ui.lb_nd_pb.text(), cf.ui.lb_da_pb.text(),
			"Bật" if (dk.s_d_pb == True) else "Tắt",
			"An toàn" if (dk.mq_on == False) else "Cảnh báo")
		# ~ elif (num == 2):
			# ~ mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nCửa: %s"\
			# ~ % ("Phòng tắm", cf.ui.lb_nd_pt.text(), cf.ui.lb_da_pt.text(),
			# ~ "Bật" if (dk.s_d_pt == True) else "Tắt",
			# ~ "Mở" if (dk.door_open_list[0] == True) else "Đóng")
		# ~ elif (num == 3):
			# ~ mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nCấp độ đèn siêu sáng: %s\nCửa: %s"\
			# ~ % ("Phòng ngủ 1", cf.ui.lb_nd_pn1.text(), cf.ui.lb_da_pn1.text(),
			# ~ "Bật" if (dk.s_d_pn1 == True) else "Tắt", dk.v_d_ss_pn1,
			# ~ "Mở" if (dk.door_open_list[1] == True) else "Đóng")
		# ~ elif (num == 4):
			# ~ mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nCấp độ đèn siêu sáng: %s\nCửa: %s"\
			# ~ % ("Phòng ngủ 2", cf.ui.lb_nd_pn2.text(), cf.ui.lb_da_pn2.text(),
			# ~ "Bật" if (dk.s_d_pn2 == True) else "Tắt", dk.v_d_ss_pn2,
			# ~ "Mở" if (dk.door_open_list[2] == True) else "Đóng")
		elif (num == 2):
			mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s"\
			% ("Phòng tắm", cf.ui.lb_nd_pt.text(), cf.ui.lb_da_pt.text(),
			"Bật" if (dk.s_d_pt == True) else "Tắt")
		elif (num == 3):
			mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nCấp độ đèn siêu sáng: %s"\
			% ("Phòng ngủ 1", cf.ui.lb_nd_pn1.text(), cf.ui.lb_da_pn1.text(),
			"Bật" if (dk.s_d_pn1 == True) else "Tắt", dk.v_d_ss_pn1)
		elif (num == 4):
			mess = "%s\nNhiệt độ: %s\nĐộ ẩm: %s\nĐèn: %s\nCấp độ đèn siêu sáng: %s"\
			% ("Phòng ngủ 2", cf.ui.lb_nd_pn2.text(), cf.ui.lb_da_pn2.text(),
			"Bật" if (dk.s_d_pn2 == True) else "Tắt", dk.v_d_ss_pn2)
		elif (num == 5):
			mess = "%s\nCường độ sáng: %s\nNhiệt độ: %s\nĐèn cầu thang: %s\nCửa trước: %s"\
			% ("Sân trước", cf.ui.lb_as_st.text(), cf.ui.lb_nd_st.text(),
			"Bật" if (dk.s_d_st == True) else "Tắt",
			"Mở" if (dk.door_open_list[3] == True) else "Đóng")
		query.edit_message_text(text = mess)
		
def echo(update: Update, context: CallbackContext) -> None:
	global in_cmd_quest, turnoff_state, hide_state
	update.message.text = update.message.text.lower()
	if (check_uid(update.message.chat.id)):
		if (update.message.text == "y" and turnoff_state == True): cf._exit(False, True)
		elif (update.message.text == "n" and turnoff_state == True):
			update.message.reply_text("Đã hủy bỏ tắt hệ thống.")
			turnoff_state = False
			in_cmd_quest = False
		elif (update.message.text == "y" and hide_state == True):
			update.message.reply_text("Hệ thống đã ẩn giao diện.")
			update.message.reply_text("Bạn vẫn có thể trả lời cuộc trò chuyện này.")
			cf.MainWindow.hide()
			in_cmd_quest = False
		elif (update.message.text == "n" and hide_state == True):
			update.message.reply_text("Đã hủy bỏ ẩn giao diện hệ thống.")
			in_cmd_quest = False
			hide_state = False
		elif (text_find(update.message.text, ["hình", "ảnh"])):
			# bot.sendPhoto(update.message.chat.id, photo=open("image/IMG_0029.JPG", "rb"))
			update.message.reply_photo(open("image/IMG_0029.JPG", "rb"))
			update.message.reply_text("Đây là hình tôi gửi cho bạn.")
		elif (text_find(update.message.text, ["yêu"])):
			update.message.reply_text("Tôi có crush nha, mà chưa ngỏ lời.")
		elif (text_find(update.message.text, ["hello", "chào", "hi", "xin chào"])):
			update.message.reply_text("Chào cậu.")
		elif (text_find(update.message.text, ["admin"])):
			text = update.message.text.split(' ')
			update.message.reply_text(
				"[Test] Cám ơn bạn đã đăng ký, bây giờ bạn có thể sử dụng toàn bộ tính năng của hệ thống.")
			list_uid.append([text[1], text[2], text[3]])
			f = open("data.txt", "a")
			f.writelines(list_uid[-1][0] + "," + list_uid[-1][1] + "," + str(list_uid[-1][2])+ ",\n")
			f.close()
		else: print(update)
	else:
		update.message.reply_text("Tài khoản của bạn chưa đăng ký, bạn không thể thực hiện chức năng này.")

def bot_start() -> None:
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("end", end))
	dispatcher.add_handler(CommandHandler("admin", bot_command))
	dispatcher.add_handler(CommandHandler("control", bot_control))
	dispatcher.add_handler(CommandHandler("info", bot_info))
	updater.dispatcher.add_handler(CallbackQueryHandler(button))
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
	updater.start_polling()
	# updater.idle()

def time_run():
	global timec
	while (True):
		timec = int(time.strftime("%S"))
		time.sleep(1)

def init():
	global list_uid
	f = open("data.txt", "r")
	for line in f.readlines():
		line = line.split(',')
		line[2] = int(line[2])
		list_uid.append(line)
	f.close()
	Thread(target = time_run).start()
