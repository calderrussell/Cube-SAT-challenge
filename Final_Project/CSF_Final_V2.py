#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2 as cv
import os
import numpy as np
from git import Repo
import time
from picamera2 import Picamera2


# In[2]:


REPO_PATH = "/home/csf/Cube-SAT-challenge"     #Your github repo path: ex. /home/pi/FlatSatChallenge
FOLDER_PATH = "/Final_Project/Images"   #Your image folder path in your GitHub repo: ex. /Images

picam2 = Picamera2()


# In[3]:


def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        print('added remote')
        origin.pull()
        print('pulled changes')
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit('New Photo')
        print('made the commit')
        origin.push()
        print('pushed changes')
    except:
        print('Couldn\'t upload to git')


# In[4]:


def img_gen(name):
    """
    This function is complete. Generates a new image name.

    Parameters:
        name (str): your name ex. MasonM
    """
    t = time.strftime("_%H%M%S")
    imgname = (f'{REPO_PATH}/{FOLDER_PATH}/{name}{t}.jpg')
    
    print("Image named")
    
    return imgname


# In[5]:


def take_photo():
    name = "CSF"  # Replace with your actual name (e.g., "MasonM")
    
    # Generate image name
    img_path = img_gen(name)

    # Take a photo
    picam2.start_and_capture_file(img_path)
    print(f"Photo saved: {img_path}")

    # Push the photo to GitHub
    # git_push()
    
    return img_path


# In[6]:


def getImageRGBAndHSV(img_path):

    #open image
    img = cv.imread(img_path)
    
    #convert to RGB and HSV
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    print("RGB and HSV images created")
    
    return img, imgRGB, hsv


# In[7]:


def createMask(img, hsv, lowerBound, upperBound):

    #create mask
#      lowerBound = np.array([40,30,40])
#     upperBound = np.array([70,255,255])
#     for green shirt
 
    mask = cv.inRange(hsv, lowerBound, upperBound)
    
    #create masked image
    masked_img = cv.bitwise_and(img, img, mask=mask)

    mask_path = img_gen("Mask")
    cv.imwrite(mask_path, masked_img)
    
    print("Mask created")
    
    return mask, masked_img


# In[8]:


def analyzeMask(mask):
    
    #create contours
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    #find largest contour
    largest_contour = max(contours, key=cv.contourArea)

    #EDIT THIS TO FIND AREA OF ALL CONTOURS COMBINED
    
    #get its area
    area = cv.contourArea(largest_contour)
    print("Mask area is", area)



# In[9]:


def showImages(img, masked_img):
    #show original image
    cv.imshow("original", img)

    #show masked image
    cv.imshow("masked_img", masked_img)
    cv.waitKey(0)


# In[10]:


def main():
    #take image
    img_name = take_photo()
    
    #makes objects for the original image, RGB, and HSV
    image, RGB_image, HSV_image = getImageRGBAndHSV(img_name)
    
    #create mask and mask combined with image 
    lowerBound = np.array([6,80,60])
    upperBound = np.array([14,255,255])
    mask, masked_img = createMask(image, HSV_image, lowerBound, upperBound)
    
    #get information on the affected area
    analyzeMask(mask)
    
    # display images
    # showImages(image, masked_img)


# In[ ]:


main()


# In[ ]:




