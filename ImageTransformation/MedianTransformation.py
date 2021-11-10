import cv2
import os

def read(filepath,filename):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)

    blurMedian=cv2.medianBlur(image,3)
    outputpath = "output_image_filepath"
    cv2.imwrite(outputpath+"3median_"+filename,blurMedian)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        read(filepath,filename)
        print(filename)

    print ("ok")