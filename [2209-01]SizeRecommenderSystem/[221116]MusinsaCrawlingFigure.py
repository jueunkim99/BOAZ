# -*- coding: utf-8 -*-
#ȯ�漳��
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import time
import pandas as pd
import warnings
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from html_table_parser import parser_functions as parser

#���Ż�->����->�ĵ�Ƽ����->���Ż���õ��->top1~5
#������ũ �ڵ� �߰� �ʿ�
#�߰� �ߴ� â ���ֱ�
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.get('https://www.musinsa.com/app/goods/2326935')
time.sleep(10)
try:
    #body > div > div > div > button > svg > path
    button = driver.find_element_by_css_selector('body > div > div > div > div > a.modal__btn.modal__btn--secondary')
    button.send_keys(Keys.ENTER)
    print("coupon close")
except:
    print("no button1")
time.sleep(5)
try:
    button2 = driver.find_element_by_css_selector('#divpop_goods_yale_8459 > form > button.btn.btn-close')
    button2.send_keys(Keys.ENTER)
except:
    print("no button2")
time.sleep(10)


#user, gender,height,weight,item, size,content, evaluation(size_eval,bright_eval,color_eval,thick_eval)
user_list = []
gender_list =[]
height_list = []
weight_list =[]
item_list = []
size_list = []
star_list= []
content_list = []
size_eval_list =[]
bright_eval_list =[]
color_eval_list =[]
thick_eval_list =[]

#�Լ�����
def get_content(driver):
    #�Լ��ȿ� html, soup �־���� ������ �Ѿ�� �ٸ��� �ܾ��, �ۿ� �������� ù�������� ������ �ܾ�����.
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    for i in range(10):
        profile_before = soup.find_all('p','review-profile__body_information')
        profile_after = profile_before[i].text.split(',')
        try:
            gender = profile_after[0]
            height = profile_after[1]
            weight = profile_after[2]
        except:
            gender = ''
            height = ''
            weight = ''


        try:
            user = soup.find_all('p','review-profile__name')[i].text
            item = soup.find_all('a','review-goods-information__name')[i].text
            # '/n' ���ְ� �����ϱ�
            size = soup.find_all('span', 'review-goods-information__option')[i].text.strip().replace('\n','')
            content = soup.find_all('div','review-contents__text')[i].text
        except:
            user = ''
            item = ''
            size = ''
            content = ''
            
        stars = driver.find_elements_by_xpath('//*[@id="reviewListFragment"]/div['+
                                              str(i+1)+']/div[3]/span/span/span')
        try:
            for j in stars:
                a =j.get_attribute('style')
                if a[7:9]=='20':
                    star = 1
                elif a[7:9]=='40':
                    star = 2
                elif a[7:9]=='60':
                    star = 3
                elif a[7:9]=='80':
                    star = 4
                else:
                    star = 5
        except:
            star = ''
      
        evaluation = soup.find_all('div', 'review-evaluation')
        try:
            size_eval = evaluation[i].find_all('span')[0].text
            bright_eval = evaluation[i].find_all('span')[1].text
            color_eval = evaluation[i].find_all('span')[2].text
            thick_eval = evaluation[i].find_all('span')[3].text
        except:
            size_eval = ''
            bright_eval = ''
            color_eval = ''
            thick_eval = ''
        
        user_list.append(user)
        gender_list.append(gender)
        height_list.append(height)
        weight_list.append(weight)
        item_list.append(item)
        size_list.append(size)
        content_list.append(content)
        star_list.append(star)
        size_eval_list.append(size_eval)
        bright_eval_list.append(bright_eval)
        color_eval_list.append(color_eval)
        thick_eval_list.append(thick_eval)
        
        
#��ư ������ �Լ�����
def move_next(driver):    
    for i in range(4):
        get_content(driver)
        #������ 2,3,4,5 �Ѿ��
        driver.find_element_by_css_selector('#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > a:nth-child(' + 
                                            str(int(4) + int(i)) + ')').send_keys(Keys.ENTER)
        time.sleep(2)
    get_content(driver)
    
#�״��� ȭ��ǥ'>'��ư������: (6,7,8...)�ִ� �������� �Ѿ��   
def move_arrow(driver):
    driver.find_element_by_css_selector('#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > a.fa.fa-angle-right.paging-btn.btn.next').send_keys(Keys.ENTER)

#������ǥ��������
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
figure = soup.find('table',{'class':'table_th_grey'})
p = parser.make2d(figure)
figure_df = pd.DataFrame(data = p[1:],columns = p[0])
figure_df.drop([0,1],inplace = True)

#ũ�Ѹ�����
#���� �������ֱ�#1->50,2->100
for i in range(1):
     try:
        move_next(driver)
        move_arrow(driver)
     except:
        time.sleep(2)
    

df = pd.DataFrame({'user':user_list, 
                   'gender':gender_list,
                   'height':height_list ,
                   'weight':weight_list,
                   'item':item_list, 
                   'size':size_list,
                   'star':star_list,
                   'content':content_list,
                   'size_eval':size_eval_list,
                   'bright_eval':bright_eval_list,
                   'color_eval':color_eval_list,
                   'thick_eval':thick_eval_list})
#������ǥ�� merge
merge_df = pd.merge(df,figure_df,how = 'left',left_on = 'size',right_on = 'cm')
merge_df.to_csv('[221116]Hood1_Test.csv')
