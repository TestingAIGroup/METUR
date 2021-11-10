import os
import xlrd
import xlwt


def write2file(List_eachNumOfError):
    output_filepath = 'E:\\githubAwesomeCode\\plantIndentification\\code\\ResultAnalysis\\data\\TestSequence4\\pictureThis\\pictureThis_All_img.xls'

    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'Sheet1', cell_overwrite_ok=True)

    i = 0  # 每张图片的结果从第二行开始写
    for list in List_eachNumOfError:
        sheet1.write(i, 0, list)
        i = i + 1
    f.save(output_filepath)

def handler(filename,All_img):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    List_Img=[] #出错的图片的名称

    for n in range(1,sheet2.nrows): #200张原始图片
        raw_picture = sheet2.row_values(n)[0]  #原始图片结果的list
        print("raw_picture:",raw_picture)
        List_Img.append(raw_picture)
        All_img.append(raw_picture)

   # print(len(All_img))
    write2file(All_img)
    return List_Img

def img_preprocess():
    filepath = 'E:\\githubAwesomeCode\\plantIndentification\\code\\ResultAnalysis\\data\\TestSequence4\\pictureThis\\output\\'
    fileList = os.listdir(filepath)  # 返回的是list

    All_img = []
    for filename in fileList:
        print(filename)
        handler(filepath + filename, All_img)

    print("ok")

def read_file(filepath):
    workbook = xlrd.open_workbook(filepath)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    list_img = []
    for n in range(0, sheet2.nrows):  # 200张原始图片
        raw_picture = sheet2.row_values(n)[0]
        list_img.append(raw_picture)

    return list_img

def error_sequence(list_img,error_img):

    total_rank=1

    for index in range(0,len(list_img)):
        for j in range(0,len(error_img)):
            if list_img[index]==error_img[j]:
                #print(list_img[index])
                total_rank=total_rank+index
                #print("index:",index)
    print("total rank:",total_rank)

    m=len(error_img)
    n=len(list_img)
    rank_mn=total_rank/(m*n)
    apfd=1-rank_mn+1/(2*n)
    print("plantSnap_APFD:",apfd)
    return apfd


if __name__ == '__main__':
    #img_preprocess()

    abs_path="E:\\githubAwesomeCode\\plantIndentification\\code\\ResultAnalysis\\data\\TestSequence4\\pictureThis\\"


    error_img_path="error\\pictureThis_error.xlsx"
    #按照测试上下文优先级顺序，参数从小到大
    all_img_path = "pictureThis_All_img.xls"
    #按照测试上下文优先级顺序，参数从大到小
    convert_img_path="pictureThis_All_img_convert.xls"
    #按照测试上下文优先级顺序，参数顺序随机
    para_random_img_path="pictureThis_All_img_para_random.xls"
    
    plantSnap_all_img=abs_path+para_random_img_path
    plantSnap_error_img=abs_path+error_img_path

    list_img=read_file(plantSnap_all_img)
    error_img=read_file(plantSnap_error_img)
    print("len of all imgs:", len(list_img))
    print("len of error imgs:", len(error_img))

    #read_file(plantSnap_all_img_path)
    error_sequence(list_img,error_img)

    """
# 随机顺序
error_img_path = "error\\pictureThis_error.xlsx"
plantSnap_error_img = abs_path + error_img_path
total = 0
for i in range(10):
    random_img_path = "random\\pictureThis_All_img_random" + str(i) + ".xls"
    plantSnap_all_img = abs_path + random_img_path
    list_img = read_file(plantSnap_all_img)
    error_img = read_file(plantSnap_error_img)
    print("len of all imgs:", len(list_img))
    print("len of error imgs:", len(error_img))

    # read_file(plantSnap_all_img_path)
    total = total + error_sequence(list_img, error_img)

print("avergae apfd:", total / 10)

"""








