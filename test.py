from PIL import ImageGrab
import cv2, sys
from matplotlib import pyplot as plt
import numpy as np

# Capture current screen
#img = ImageGrab.grab()
img = cv2.imread('Img.PNG', cv2.IMREAD_GRAYSCALE)
dead = cv2.imread('dead.PNG', cv2.IMREAD_GRAYSCALE)

# Resize and crop image
img = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)
totX = len(img[0])
totY = len(img)
img = img[int(totY*0.42):int(totY*0.78),int(totX*0.11):int(totX*0.46)]

# Blur image
blur = cv2.GaussianBlur(img, ksize=(5,5), sigmaX=0)
ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

print(blur[-1][1])
plt.clf()
plt.imshow(thresh1, cmap='Greys_r')
plt.show()
