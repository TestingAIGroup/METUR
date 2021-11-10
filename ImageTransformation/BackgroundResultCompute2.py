# coding:utf-8
import xlrd
import xlwt
import re


def result2file(List_eachNumOfError, numOfError):
    output_filepath = 'E:\\githubAwesomeCode\\plantIndentification\\code\\ResultAnalysis\\data\\0510result\\bg\\plantNet_bg_top-1_result.xls'
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 1, numOfError)  # 总的结果在第一行

    i = 1  # 每张图片的结果从第二行开始写
    for list in List_eachNumOfError:
        sheet1.write(i, 0, list)
        i = i + 1
    f.save(output_filepath)


# top-1结果分析
def handler_excel(filename):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    numOfError = 0  # 出错的总数量
    List_eachNumOfError = []  ##每一张raw图片，构造的衍生图片出错的数量, 构成的list

    for n in range(200):  # 200张原始图片
        raw_picture = sheet2.row_values(9 * n + 1)  # 原始图片结果的list
        print(raw_picture)
        raw_first = raw_picture[1]  # 原始图片的top-1结果
        print(raw_first)
        eachNumOfError = 0  # 每一张raw图片，构造的衍生图片出错的数量

        List_eachNumOfError.append(raw_picture[0])  # 图片名称作为分隔

        for i in range(2, 10):
            follow_picture = sheet2.row_values((9 * n + i))  # 衍生图片结果的list
            follow_first = follow_picture[1]  # 衍生图片的top-1结果
            print(follow_first)
            if str(raw_first) != str(follow_first):
                eachNumOfError = eachNumOfError + 1
                numOfError = numOfError + 1

        List_eachNumOfError.append(eachNumOfError)
        print(eachNumOfError)

    print(numOfError)

    result2file(List_eachNumOfError, numOfError)


################################################################################################

def result2file_top3(ALL_eachDis, each_total_result, each_average_result):
    output_filepath = './data/0510result/mobicase_result/plantNet_bg_top-3_result2.xls'
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'Sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 1, "result")  # 总的结果在第一行

    total,average=compute_total(each_average_result,200)

    for n in range(200):
        sheet1.write(9 * n + 1, 1, each_total_result[n])
        sheet1.write(9 * n + 1, 2, each_average_result[n])
        sheet1.write(0,2,average)

    i = 1  # 每张图片的结果从第二行开始写
    for list in ALL_eachDis:
        sheet1.write(i, 0, list)
        i = i + 1
    f.save(output_filepath)


# top-3结果分析
def handler_excel_top3(filename):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    each_total_result = [];
    each_average_result = [];  # 每张raw图片的total和average 的Jaccard dissimilarity结果，构成的list

    ALL_eachDis = []  ##所有！ 构造的衍生图片与原始图片的Jaccard dissimilarity, 构成的list

    for n in range(200):  # 200张原始图片

        raw_result = []  # 原始图片结果的list,不包含图片名,没有结果的就是空
        raw_picture = sheet2.row_values(9 * n + 1)  # 原始图片结果的list,包含图片名
        print(raw_picture)
        raw_result.append(raw_picture[1]);
        raw_result.append(raw_picture[2]);
        raw_result.append(raw_picture[3]);

        real_RawResult = remove_none(raw_result)
        print(real_RawResult)

      #  ALL_eachDis.append(raw_picture[0])  # 用图片名分隔结果
        List_eachDis = []  ##每一张raw图片，构造的衍生图片与原始图片的Jaccard dissimilarity, 构成的list

        for i in range(2, 10):
            follow_result = []  # 衍生图片结果的list，包含图片名
            follow_picture = sheet2.row_values((9 * n + i))  # 衍生图片结果的list，包含图片名
            follow_result.append(follow_picture[1]);
            follow_result.append(follow_picture[2]);
            follow_result.append(follow_picture[3]);

            real_FollowResult = remove_none(follow_result)

            # 计算 Jaccard dissimilarity
            dis_similarity = compute_jaccardDis(real_RawResult, real_FollowResult)
            print(dis_similarity)

            List_eachDis.append(dis_similarity)
            ALL_eachDis.append(dis_similarity)  # 保存所有的结果

        # 计算每张raw图片的total和average dis
        each_total, each_average = compute_total_each(List_eachDis,8)
        each_total_result.append(each_total);each_average_result.append(each_average) #200个total结果和200个average结果

    result2file_top3(ALL_eachDis, each_total_result, each_average_result)


# 计算每张raw图片的dis
def compute_total_each(list,num):
    total = 0
    for dis in list:
        if isnumber(dis):
            total = total + dis
    print(total)
    average = total / num
    print(average)
    return total, average


# 计算平均值
def compute_total(list,num):
    total = 0
    for dis in list:
        if isnumber(dis):
            total = total + dis
    print(total)
    average = total / num
    print(average)
    return total, average


def isnumber(aString):
    try:
        float(aString)
        return True
    except:
        return False


# 去除list中的空元素
def remove_none(temp_list):
    return_list = [i for i in temp_list if (len(str(i)) != 0)]
    return return_list


def compute_jaccardDis(x, y):  # x是source的结果,y是follow的结果
    res = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    # 计算的是不相似程度
    dis_similarity = 1 - res / float(union_cardinality)
    return dis_similarity


if __name__ == '__main__':
    fileName = 'E:\\githubAwesomeCode\\plantIndentification\\code\\ResultAnalysis\\data\\0510result\\bg\\plantNet\\plantNet_bg.xls'
    # handler_excel(fileName)  # top-1结果分析

    handler_excel_top3(fileName)


























