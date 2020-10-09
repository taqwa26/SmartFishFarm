import cv2
import numpy as np
 
img = cv2.imread('circles.png', 1)
hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
lower_range = np.array([30, 150, 50], dtype=np.uint8)
upper_range = np.array([255, 255, 180], dtype=np.uint8)
mask = cv2.inRange(hsv, lower_range, upper_range)
res = cv2.bitwise_and(img,img, mask= mask)
 
#cv2.imshow('mask',mask)
#cv2.imshow('image', img)

cv2.imshow('mask',mask)

cv2.imshow('image', img)

cv2.imshow('res', res)
 
while(1):
  k = cv2.waitKey(0)
  if(k == 27):
    break
 
cv2.destroyAllWindows()