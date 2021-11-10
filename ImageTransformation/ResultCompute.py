# coding:utf-8
import xlrd
import xlwt
import re


def result2file(List_eachNumOfError, numOfError):
    output_filepath = 'output_path'
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'Sheet1', cell_overwrite_ok=True)
    sheet1.write(0, 1, numOfError)  

    i = 1 
    for list in List_eachNumOfError:
        sheet1.write(i, 0, list)
        i = i + 1
    f.save(output_filepath)


# top-1 results
def handler_excel(filename):
   
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    numOfError = 0  
    List_eachNumOfError = []  

    for n in range(200): 
        raw_picture = sheet2.row_values(9 * n + 1)  
        print(raw_picture)
        raw_first = raw_picture[1]  
        print(raw_first)
        eachNumOfError = 0 

        List_eachNumOfError.append(raw_picture[0])  

        for i in range(2, 10):
            follow_picture = sheet2.row_values((9 * n + i))  
            follow_first = follow_picture[1] 
            print(follow_first)
            if str(raw_first) != str(follow_first):
                eachNumOfError = eachNumOfError + 1
                numOfError = numOfError + 1

        List_eachNumOfError.append(eachNumOfError)
        print(eachNumOfError)

    print(numOfError)

    result2file(List_eachNumOfError, numOfError)


################################################################################################

# top-3 results
def result2file_top3(ALL_eachDis, each_total_result, each_average_result):
    output_filepath = 'output_path'
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'Sheet1', cell_overwrite_ok=True)

    sheet1.write(0, 1, "result")  

    total,average=compute_total(each_average_result,200)

    for n in range(200):
        sheet1.write(9 * n + 1, 1, each_total_result[n])
        sheet1.write(9 * n + 1, 2, each_average_result[n])
        sheet1.write(0,2,average)

    i = 1  
    for list in ALL_eachDis:
        sheet1.write(i, 0, list)
        i = i + 1
    f.save(output_filepath)



def handler_excel_top3(filename):
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet2 = workbook.sheet_by_name(index)

    each_total_result = [];
    each_average_result = [];  

    ALL_eachDis = []  

    for n in range(200):  

        raw_result = [] 
        raw_picture = sheet2.row_values(9 * n + 1)  
        print(raw_picture)
        raw_result.append(raw_picture[1]);
        raw_result.append(raw_picture[2]);
        raw_result.append(raw_picture[3]);

        real_RawResult = remove_none(raw_result)
        print(real_RawResult)

      #  ALL_eachDis.append(raw_picture[0]) 
        List_eachDis = [] 

        for i in range(2, 10):
            follow_result = []  
            follow_picture = sheet2.row_values((9 * n + i))  
            follow_result.append(follow_picture[1]);
            follow_result.append(follow_picture[2]);
            follow_result.append(follow_picture[3]);

            real_FollowResult = remove_none(follow_result)

            # 计算 Jaccard dissimilarity
            dis_similarity = compute_jaccardDis(real_RawResult, real_FollowResult)
            print(dis_similarity)

            List_eachDis.append(dis_similarity)
            ALL_eachDis.append(dis_similarity)  

        # 计算每张raw图片的total和average dis
        each_total, each_average = compute_total_each(List_eachDis,8)
        each_total_result.append(each_total);each_average_result.append(each_average) 

    result2file_top3(ALL_eachDis, each_total_result, each_average_result)


def compute_total_each(list,num):
    total = 0
    for dis in list:
        if isnumber(dis):
            total = total + dis
    print(total)
    average = total / num
    print(average)
    return total, average


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


# 
def remove_none(temp_list):
    return_list = [i for i in temp_list if (len(str(i)) != 0)]
    return return_list


def compute_jaccardDis(x, y): 
    res = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    dis_similarity = 1 - res / float(union_cardinality)
    return dis_similarity


if __name__ == '__main__':
    fileName = 'result_path'
    # handler_excel(fileName)  

    handler_excel_top3(fileName)


























