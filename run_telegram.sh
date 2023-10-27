cd "/home/triet073/Desktop/telegram project/"
while :
do
	notify-send "Hệ thống đang khởi động..."
	pkill audacious
	pkill python3
	python3 reset_led.py
	python3 main.py
done
#~ pkill python3
#~ notify-send "Hệ thống đã tắt"
