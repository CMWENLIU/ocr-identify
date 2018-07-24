import numpy as np
import re
import itertools
from collections import Counter
import pyocr
import pyocr.builders
import PIL
from PIL import Image


def clean_str(string):

    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def process_raw(string):

    string = re.sub(' +',' ', string)
    string = string.replace('\n', '')
    return string.strip().lower()

def ext_txt(img, languages, tool):
    rlist = []
    for l in languages:
        txt = tool.image_to_string(img, lang=l, builder=pyocr.builders.TextBuilder())
        cleaned = process_raw(txt)
        rlist.append(cleaned)
    return list(zip(languages, rlist))
    
