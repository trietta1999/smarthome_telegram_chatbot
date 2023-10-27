import cv2

cap = cv2.VideoCapture(1)

while (True):
	s, img = cap.read()
	cv2.imshow("img1", img)
	cv2.waitKey(1)
