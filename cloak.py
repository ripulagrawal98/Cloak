import numpy as np
import cv2

import time

cap = cv2.VideoCapture(0)

time.sleep(2)

background = 0

for i in range(30):
  ret,background = cap.read()
# print(background)
# print(ret)

while(cap.isOpened()):
  ret,img = cap.read()

  if not ret:
    break

  hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

  lower_red = np.array([0,120,70]) 
  upper_red = np.array([10,255,255])
  mask1 = cv2.inRange(hsv,lower_red, upper_red)

  lower_red = np.array([170,120,70])
  upper_red = np.array([180,255,255])
  mask2 = cv2.inRange(hsv,lower_red,upper_red)

  mask1 = mask1 + mask2

  green_lower = np.array([25, 50, 72], np.uint8) 
  green_upper = np.array([102, 255, 255], np.uint8) 
  green_mask = cv2.inRange(hsv, green_lower, green_upper) 
  
    # Set range for blue color and 
    # define mask 
  blue_lower = np.array([94, 80, 2], np.uint8) 
  blue_upper = np.array([120, 255, 255], np.uint8) 
  blue_mask = cv2.inRange(hsv, blue_lower, blue_upper) 



  ## mask o yellow (15,0,0) ~ (36, 255, 255)
  mask = cv2.inRange(hsv, (15,0,0), (36, 255, 255))
  ## final mask and masked
  mask1 = cv2.bitwise_or(mask1, green_mask)
  mask1 = cv2.bitwise_or(mask1,blue_mask)


  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations = 2)
  mask2 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations = 1)

  mask2 = cv2.bitwise_not(mask1)

  res1 = cv2.bitwise_and(background,background,mask = mask1)
  res2 = cv2.bitwise_and(img,img,mask = mask2)
  final_output = cv2.addWeighted(res1,1,res2,1,0)

  cv2.imshow("Invisible",final_output)
  k = cv2.waitKey(10)
  if k == 27:
    break

cap.release()
cv2.destroyAllWindows()