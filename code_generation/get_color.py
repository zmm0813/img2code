#coding=utf-8
import numpy
from PIL import Image

def get_color(img,No):
    img = numpy.array(img)
    width = img.shape[1]
    height = img.shape[0]
    y = int(2*height/3)
    if No == 1:
        rgb=(img[y][1][0],img[y][1][1],img[y][1][2])
    elif No==2:
        x = int(width*9/12)
        rgb=(img[y][x][0],img[y][x][1],img[y][x][2])
    return str(rgb)



