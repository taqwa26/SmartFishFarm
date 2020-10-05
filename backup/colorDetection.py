import time
#Import OpenCV
import cv2
#Import Numpy
import numpy as np
#Baca gambar
img = cv2.imread('jeruk.jpeg')
#Konversi RGB ke HSV
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#Range warna kuning segmentasi/klasifikasi
lower = np.array([20,100,100], dtype=np.uint8)
upper = np.array([40,255,255], dtype=np.uint8)
mask = cv2.inRange(hsv, lower, upper)
kernel = np.ones((25,25),np.uint8)
#Dipertembal piksel objek
dilation = cv2.dilate(mask,kernel,iterations = 1)
#Diperkecil supaya tidak berdempet piksel objeknya
erosion = cv2.erode(img,kernel,iterations = 1)
#Temukan kontut
contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#Kopi gambar asli ke variable resultImg
resultImg = (img).copy()
#Array kontur
contour = []
#Perulangan untuk kontur
for i in range(len(contours)):
        #Banyaknya kontur ke variable cnt
        cnt = contours[i]
        #Mencari radius untuk menggambar lingkaran
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        #Pusat lingkaran
        center = (int(x),int(y))
        #Jika radius(kontur ukuran > 1 ) diaanggap kontur jika kurang bukan kontur
        if(int(radius) > 1):
            contour.append(cnt)
            #Gambar lingkaran
            resultImg = cv2.circle(resultImg,center,int(radius),(255,0,0),3)
#Tampilkan
if mask.any():
    #cv2.imshow("Jeruk Found", resultImg)
    print('Jeruk Found!!')
else:
    #cv2.imshow("Jeruk Not Found", resultImg)
    print('Jeruk Not Found!!')
    
#delay    
time.sleep(5)
#stop
exit()