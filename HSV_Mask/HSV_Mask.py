import cv2 as cv
import os
import numpy as np
import matplotlib.pyplot as plt


def hsvColorSegmentation():

    #open image
    img = cv.imread("/home/minjae/Documents/Code/Python/Projects/HSV_Mask/Cambridge Space Force_132042.jpg")
    
    #convert to RGB and HSV
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #create mask
    lowerBound = np.array([40,30,40])
    upperBound = np.array([70,255,255])
    mask = cv.inRange(hsv, lowerBound, upperBound)
    
    #create masked image
    masked_img = cv.bitwise_and(img, img, mask=mask)

    #create contours
    contours, herarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #find largest contour
    largest_contour = max(contours, key=cv.contourArea)

    #get its area
    area = cv.contourArea(largest_contour)
    print("Mask area is", area)

    #show all contours in green
    cv.drawContours(masked_img, contours, -1, (0, 0, 255), 1)
    
    #show largest contour in red
    cv.drawContours(masked_img, largest_contour, -1, (0,255,0), 3)

    #show original image
    plt.figure()
    plt.imshow(imgRGB)
    plt.show()

    #show masked image
    cv.imshow("masked_img", masked_img)
    cv.waitKey(0)



if __name__ == '__main__':
    hsvColorSegmentation()

