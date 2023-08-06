import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np


def Check_Screen(image):
    wimage = np.full((185, 279,3), 178, dtype = np.uint8)# ----> ((788-358)+1, (948-421)+1)
    
    bimage = np.full((185, 279,3), 92, dtype = np.uint8)
    #image = cv2.imread('Image_75.jpeg')
    #image = cv2.imread('6.jpeg')
    wimage = cv2.cvtColor(wimage, cv2.COLOR_BGR2GRAY)
    bimage = cv2.cvtColor(bimage, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    height, width = image.shape
    upper_left = (657, 269)#--->in paint (421,358)
    bottom_right = (935, 453)#--->in paint (948,788)
    img = image[upper_left[1]: bottom_right[1] + 1, upper_left[0]: bottom_right[0] + 1]
    print(img.shape)
    (score, diff) = ssim(wimage, img, full=True)
    (score1, diff1) = ssim(bimage, img, full=True)
    print(score, score1)
    if score>score1:
        print("Screen is on")
        #return True
    else:
        print("Screen is off")
        #return False