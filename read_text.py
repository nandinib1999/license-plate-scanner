# pytesseract is for OCR from images
# Check PyPi Project - https://pypi.org/project/pytesseract/
import pytesseract

# OpenCV for pre-processing images before feeding to the tesseract OCR.
# Check PyPi Project - https://pypi.org/project/opencv-python/
import cv2

import numpy as np

from yolo_object import detect_license_plate

import numpy as np
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from deskew import determine_skew

# Including the path to the tesseract.exe for PyTesseract to work
pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
# PyTesseract Config Options
# language = English
# psm or Page segmentation modes = 7 represents treat the image as a single line text
# oem or Engine Mode - Nueral Nets LSTM engine only
config = ('-l eng --oem 1 --psm 7')

def crop_image_only_outside(img,tol=0):
    # img is 2D image data
    # tol  is tolerance
    mask = img>tol
    m,n = img.shape
    mask0,mask1 = mask.any(0),mask.any(1)
    col_start,col_end = mask0.argmax(),n-mask0[::-1].argmax()
    row_start,row_end = mask1.argmax(),m-mask1[::-1].argmax()
    return img[row_start:row_end,col_start:col_end]

def secondCrop(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours,_ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    if(len(areas)!=0):
        max_index = np.argmax(areas)
        cnt=contours[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        bounds = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        secondCrop = img[y:y+h,x:x+w]
    else:
        secondCrop = img
    return secondCrop



def read_text(img):
    # img = cv2.imread('images/img7.jpg')
    img = detect_license_plate(img)
    second_img = secondCrop(img)
    img = cv2.resize(second_img, None, fx=7, fy=7, interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img,(5,5),0)
    r, threshold = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite('test.png', threshold)
    image = io.imread('test.png')
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    text = pytesseract.image_to_string(rotated, config=config)
    print(text)
    return text
    # cv2.imshow("Image", rotated)
    # cv2.waitKey(0)
    # text = read_text(img)

if __name__ == '__main__':
    read_text()