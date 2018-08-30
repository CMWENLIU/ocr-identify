# import all tools and libraries
import os
#import cv2
import glob
#import spacy
import time
import datetime
import data_helpers
#import process_image
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import PIL
from PIL import Image
from random import randint
import matplotlib
import matplotlib.pyplot as plt
#import pillowfight
import numpy as np
import pandas as pd
import sys
import pyocr
import pyocr.builders

%matplotlib inline
print('All tools are imported successfully')

# Next is to prepare Tesseract OCR tools
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print('There are 130 languages available!')
print('We will use following languages:')
print(*langs, sep = '\n')


# build globle variables:
all_res = [] 
dic = {'file': '-'}
for l in langs:
    dic[l] = '-'
files_grabbed = []


# ** This step is optional for real dataset
# Clean database, remove images with low quality of text recognition
all_files = [] #create list for all files
# Load all type of available image files
ftypes = ('images/*.jpg', 'images/*.png','images/*.bmp', 'images/*.jpeg',
          'images/*.JPG', 'images/*.PNG', 'images/*.BMP', 'images/*.JPEG') 
for files in ftypes:
    all_files.extend(glob.glob(files))
print ('There are ' + str(len(all_files)) + ' images loaded')

# Remove all images which has text less than 15 characters
count = 1
for f in all_files:
    #if count % 10 == 0 or count > (len(all_files)//10)*10:
    print(str(count) + '/' + str(len(all_files)) + ': ' + f + ' is being processed!')
    try:
        result = data_helpers.ext_txt(f, langs, dic, tool)
        total_length = 0
        for l in langs:
            length = len(result[l])
            total_length += length
        if total_length < 15:
            os.remove(f)
    except:
        os.remove(f)
    count += 1
all_files = []
for files in ftypes:
    all_files.extend(glob.glob(files))
print ('After clean, there are ' + str(len(all_files)) + ' images now')



#-Load all images files for detection
ftypes = ('images/*.jpg', 'images/*.png','images/*.bmp', 'images/*.jpeg',
          'images/*.JPG', 'images/*.PNG', 'images/*.BMP', 'images/*.JPEG') 

for files in ftypes:
    files_grabbed.extend(glob.glob(files))

print ('There are ' + str(len(files_grabbed)) + ' images loaded')




#Following we recognize all images and write to database.
print('Following we recognize all images and write all text to database.')
i = 1
for f in files_grabbed:
    result = data_helpers.ext_txt(f, langs, dic, tool)
    time_str = datetime.datetime.now().isoformat()
    if i % 10 == 0 or i > (len(files_grabbed)//10)*10:
        print("{}: {}/{} processed".format(time_str, i, len(files_grabbed),))
    all_res.append(result.copy())
    i += 1

#Save result to csv file and html file for easy read
df = pd.DataFrame(all_res)
df.to_csv('result.csv', encoding='utf-8', header=True, columns=['file', 'eng', 'fra', 'spa','chi_sim'], index=False)
print('All images have been recognized and saved to result.csv')

with open('result.html', 'w', encoding = 'utf-8') as outf:
    with open('htmlhead.txt', 'r') as fh:
        for line in fh:
            outf.write(line)
    imghead = '<img src="'
    imgtail = '" onclick="changesize(this)">'
    for item in all_res:
        outf.write(imghead + item['file'] + imgtail)
        outf.write('<p>--English:' + item['eng'] + '</p>' + '\n')
        outf.write('<p>--French:' + item['fra']+ '</p>' + '\n')
        outf.write('<p>--Spanish:' + item['spa'] + '</p>' + '\n')
        outf.write('<p>--Chinese:' + item['chi_sim'] + '</p>' + '\n')
        outf.write('<hr>' + '\n')
    with open('htmltail.txt', 'r') as ft:
        for line in ft:
            outf.write(line)
print('All images have been recognized and saved to result.html')


