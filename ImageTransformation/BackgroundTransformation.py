import requests
import os

def backgroundTransform(filepath,filename):
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(filepath+filename, 'rb'),
                     'bg_image_file':open('background_image_filepath','rb')
            },
            data={'size': 'auto'},

            headers={'X-Api-Key': 'Api_key'},
        )
        if response.status_code == requests.codes.ok:
            with open('output_image_filepath'+filename+'_bg_6.jpg', 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)

if __name__ == '__main__':
    filepath = 'All_image_filepath'
    fileList = os.listdir(filepath)

    for filename in fileList:
        backgroundTransform(filepath,filename)
        print(filename)

    print ("ok")