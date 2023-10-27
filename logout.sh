#!/bin/sh

notify-send "Hệ thống đã đăng xuất"
pkill audacious
pkill python3
echo > pwm_control
#~ clear
#~ notify-send "Hệ thống đang khởi động..."
#~ python3 main.py
