from PIL import ImageGrab, Image
import cv2, sys
from matplotlib import pyplot as plt
import numpy as np
import win32api, win32con
import pytesseract

# Global parameters
screenX = 0    # width of captured screen
screenY = 0    # height of captured screen

# Initialize global parameters
img = ImageGrab.grab()
img = np.array(img)
screenX = win32api.GetSystemMetrics(0)
screenY = win32api.GetSystemMetrics(1)

# Test images
img = cv2.imread('Img.PNG', cv2.IMREAD_GRAYSCALE)
en = cv2.imread('end_normal.PNG', cv2.IMREAD_GRAYSCALE)
ed = cv2.imread('end_daily_highscore.PNG', cv2.IMREAD_GRAYSCALE)
eh = cv2.imread('end_highscore.PNG', cv2.IMREAD_GRAYSCALE)

#---------------------------------------#
#  Methods for game control             #
#---------------------------------------#

# Click the middle of the screen (move Daddy)
def click():
    win32api.SetCursorPos((int(screenX/2), int(screenY/2)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,int(screenX/2),int(screenY/2),0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,int(screenX/2),int(screenY/2),0,0)
    return

# Click the restart button
def restart():
    restartX = int(screenX*0.96)
    restartY = int(screenY*0.93)
    win32api.SetCursorPos((restartX, restartY))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,restartX,restartY,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,restartX,restartY,0,0)
    return

#---------------------------------------#
#  Methods for game state detection     #
#---------------------------------------#

# Extract daddy image and gameover information
def read_screen():
    # Resize and crop Daddy's image
    #game_screen = cv2.cvtColor(np.array(ImageGrab.grab().convert('RGB')), cv2.COLOR_RGB2GRAY)
    game_screen = ed
    tmp_img = cv2.resize(game_screen, (0,0), fx = 0.5, fy = 0.5)
    totX = len(tmp_img[0])
    totY = len(tmp_img)
    tmp_daddy = tmp_img[int(totY*0.42):int(totY*0.78),int(totX*0.11):int(totX*0.46)]

    # Blur image
    blur = cv2.GaussianBlur(tmp_daddy, ksize=(5,5), sigmaX=0)
    ret, daddy = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    # Gameover information
    # cf> white: 249, red: 134, blue: 136, gold: 192 (greyscale)
    isOver = (blur[int(len(blur)*0.1)][int(len(blur[0])*0.1)] != 249)\
        and (blur[int(len(blur)*0.1)][int(len(blur[0])*0.9)] != 249)\
        and (blur[int(len(blur)*0.9)][int(len(blur[0])*0.1)] != 249)\
        and (blur[int(len(blur)*0.9)][int(len(blur[0])*0.9)] != 249)
    return isOver, daddy

# Read score
def extract_score():
    dead_img = cv2.cvtColor(np.array(ImageGrab.grab().convert('RGB')), cv2.COLOR_RGB2GRAY)
    totX = len(dead_img[0])
    totY = len(dead_img)
    score_img = dead_img[int(totY*0.03):int(totY*0.1),0:int(totX*0.32)]
    res, thresh = cv2.threshold(score_img, 127, 255, cv2.THRESH_BINARY)
    res_string = pytesseract.image_to_string(Image.fromarray(thresh), config='digits')
    score = res_string.split('M')[0]
    print("score: "+score)
    return float(score)

#---------------------------------------#
#  Methods for debugging                #
#---------------------------------------#

def printImg(arg_img):
    plt.clf()
    plt.imshow(arg_img, cmap='Greys_r')
    plt.show()
    return

