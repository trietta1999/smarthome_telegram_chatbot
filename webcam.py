import os, cv2, time
from threading import Thread
from platform import system
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn

video = cap1 = cap2 = img1 = img2 = ''

class CamHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','multipart/x-mixed-replace; boundary=jpgboundary')
		self.end_headers()
		while (True):
			try:
				img = cv2.vconcat([img1, img2])
				img_str = cv2.imencode('.jpg', img)[1].tostring()
				self.send_header('Content-type','image/jpeg')
				self.end_headers()
				self.wfile.write(img_str)
				self.wfile.write(b"\r\n--jpgboundary\r\n")
			except: pass
           
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def server_run():
	server = ThreadedHTTPServer(("", 8000), CamHandler)
	print("Camera Server da khoi dong.")
	server.serve_forever()

def init():
	global video, cap1, cap2
	try:
		cap1 = cv2.VideoCapture(0)
		cap2 = cv2.VideoCapture(1)
	except:
		cap1 = cv2.VideoCapture(0)
	
	width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)) * 2
	height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
	video = cv2.VideoWriter("video_export.avi", cv2.VideoWriter_fourcc(*"MJPG"), 20, (width, height))
	
	Thread(target = server_run).start()
	
def destroy():
	global video, cap1, cap2
	cap1.release()
	try:
		cap2.release()
	except: pass
	video.release()
	video = cap1 = cap2 = ''

def get_img():
	global video, img1, img2
	try:
		s1, img1 = cap1.read()
		s2, img2 = cap2.read()
		img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]), interpolation = cv2.INTER_AREA)

		img1 = cv2.putText(img1, "CAM1" + time.strftime(" %H:%M:%S"), (5, img1.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
		img2 = cv2.putText(img2, "CAM2" + time.strftime(" %H:%M:%S"), (5, img2.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
	except:
		s, img = cap1.read()
		img = cv2.putText(img, "CAM1" + time.strftime(" %H:%M:%S"), (5, img1.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
		
		img1 = img2 = img
	
	con_img = cv2.hconcat([img1, img2])
	video.write(con_img)
	
	return img1, img2
	
def cvtRGB():
	c_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
	c_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
	return c_img1, c_img2
