import cv2
import numpy as np
import os

def read(filepath,filename):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)
    contrast_demo(image,1,-80,filename)

def contrast_demo(img1, c, b,filename):
    outputpath="output_image_filepath"
    rows, cols, chunnel = img1.shape
    blank = np.zeros([rows, cols, chunnel], img1.dtype)
    dst = cv2.addWeighted(img1, c, blank, 1 - c, b)

    cv2.imwrite(outputpath+"-80brightness_"+filename,dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        read(filepath,filename)
        print(filename)

    print ("ok")