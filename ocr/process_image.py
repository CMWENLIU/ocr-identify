import cv2
import numpy as np
import sys
import os.path

def rescale(img):
    newimg = cv2.resize(img,None,fx=1.2, fy=1.2, interpolation = cv2.INTER_LINEAR)
    #cv2.imwrite( "new.png", img )
    return newimg

def binarize(img):
    newimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return newimg

def remove_noise(img):
    newimg = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    return newimg

def improve(input_file):
    # Load the image
    orig_img = cv2.imread(input_file)
    output_file = binarize(orig_img)
    #output_file = remove_noise(output_file)
    #output_file = rescale(output_file)
    return output_file
