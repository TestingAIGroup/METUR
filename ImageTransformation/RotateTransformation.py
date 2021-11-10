import cv2
import os

def read(filepath,filename):
    image=cv2.imread(filepath+filename, cv2.IMREAD_COLOR)

    height,width=image.shape[:2]

    M=cv2.getRotationMatrix2D((width/2.0,height/2.0),30,1)
    rotate=cv2.warpAffine(image,M,(width,height))
    outputpath = "output_image_filepath"
    cv2.imwrite(outputpath+"30rotate_"+filename,rotate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        read(filepath,filename)
        print(filename)

    print ("ok")