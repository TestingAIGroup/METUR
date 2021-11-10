#!/usr/bin/env python
# encoding: utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
from pdb import set_trace as bp
import re
import time
import csv

'''
plantSnap： com.fws.plantsnap2
plantNet org.plantnet
pictureThis： cn.danatech.xingseus
'''

app_name="cn.danatech.xingseus"

outputFileName = "E:\githubAwesomeCode\plantIndentification\code\crawl\extraRawReview\\"+app_name
link = "https://play.google.com/store/apps/details?id="+app_name+"&hl=en_US&showAllReviews=true"
driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
driver.get(link)

flag= 0
# 点击下拉菜单
driver.find_element_by_class_name("eU809d").click()
time.sleep(1)  # 不sleep就会报错！！
# 选中需要的按钮栏‘newest’
driver.find_element_by_xpath("//div[@class='OA0qNb ncFHed']/div[@data-value='2']").click()
time.sleep(1)

click_time=0
ok=True
while 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        loadMore = driver.find_element_by_xpath("//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]").click() #"//*[contains(@class,'U26fgb O0WRkf oG5Srb C0oVfc n9lfJ')]"
        click_time+=1
        time.sleep(2)
    except:
        time.sleep(1)
        flag = flag+1
        if flag >= 10:
            break
    else:
        flag = 0

    if click_time % 50==1:
    #if ok==True:

        reviews = driver.find_elements_by_xpath("//*[@jsname='fk8dgd']//div[@class='d15Mdf bAhLNe']")
        print("click time "+str(click_time))
        print("There are "+str(len(reviews))+" reviews avaliable")
        print("Writing the data...")

        with open(outputFileName+str(click_time)+'.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["name", "ratings", "date", "comment"])
            for review in reviews:
                try:
                    soup = BeautifulSoup(review.get_attribute("innerHTML"), "lxml")
                #name = soup.find(class_="X43Kjb").text
                    ratings = soup.find('div', role='img').get('aria-label').strip("Rated ")[0]
                    date = soup.find(class_="p2TkOb").text
                    comment = soup.find('span', jsname='fbQN7e').text
                    if not comment:#expand the comment button
                        comment = soup.find('span', jsname='bN97Pc').text
                    writer.writerow([ratings.encode('utf-8'), date, comment.encode('utf-8')])
                except:
                    writer.writerow([ratings.encode('utf-8'), date, comment.encode('utf-8')])
                    print("error")

        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

