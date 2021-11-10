import cv2
import os

def read(filepath,filename):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)

    blurBilateral=cv2.bilateralFilter(image,9,75,75)
    outputpath = "output_image_filepath"
    cv2.imwrite(outputpath+"bilateral_"+filename,blurBilateral)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)
    for filename in fileList:
        read(filepath,filename)
        print(filename)

    print ("ok")