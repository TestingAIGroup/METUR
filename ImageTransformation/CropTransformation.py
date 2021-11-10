import cv2
import os
import re

def read(filepath,filename,pic_name):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)
    height, width = image.shape[:2]
    print(height,width)
    scale_demo(image,height,width,pic_name)

def scale_demo(image,height,width,pic_name):

    outputpath = "output_image_filepath"
    n=8
    y0=int(height*(n/32))
    y1=int(height*((32-n)/32))
    x0 = int(width * (n / 32))
    x1 = int(width * ((32 - n) / 32))
    print(y0)
    print(y1)
    print(x0)
    print(x1)

    dst=image[y0:y1,x0:x1]
    cv2.imwrite(outputpath + pic_name+"_8crop.jpg", dst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        print(filename)
        pic_name = re.findall(r"(.*).jpg", filename)[0]
        print(pic_name)
        read(filepath,filename,pic_name)



    print ("ok")