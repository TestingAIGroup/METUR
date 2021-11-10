import cv2
import numpy as np
import os

def read(filepath,filename):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)

    height, width = image.shape[:2]
    x=60
    y=60
    M = np.float32([[1,0,x],[0,1,y]])
    dst = cv2.warpAffine(image, M, (width, height))
    outputpath = "output_image_filepath"
    cv2.imwrite(outputpath+"60translation_"+filename,dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        read(filepath,filename)
        print(filename)

    print ("ok")