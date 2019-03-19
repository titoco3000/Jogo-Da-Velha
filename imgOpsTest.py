from PIL import ImageGrab, ImageOps
import pyautogui
import time
from numpy import *

class Cordinates():
    replayBtn = (480, 400)
    dinosaur = (246, 405)
    # x = 320 (cordinate to check for tree)
    # y = 415 (cordinate of half tree

def restartGame():
    pyautogui.click(Cordinates.replayBtn)

def pressSpace():
    pyautogui.keyDown('space')
    time.sleep(0.05)
    print('Jump')
    pyautogui.keyUp('space')

def imageGrab():
    box = (Cordinates.dinosaur[0] + 74, Cordinates.dinosaur[1], Cordinates.dinosaur[0] + 100, Cordinates.dinosaur[1]+30)
    image = ImageGrab.grab(box)
    grayImage = ImageOps.grayscale(image)
    a = array(grayImage.getcolors())
    print(a.sum())
    return(a.sum())


restartGame()
while True:
    if(imageGrab() != 1027):
        pressSpace()
        time.sleep(0.1)
