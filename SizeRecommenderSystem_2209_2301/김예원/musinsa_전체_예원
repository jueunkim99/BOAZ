import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
import time
import re
import csv
import warnings
warnings.filterwarnings('ignore')

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('headless')
# chrome_options.add_argument("disable-gpu")
# chrome_options.add_argument("'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'")
# chrome_options.add_experimental_option("detach", True)

# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# service = Service(executable_path=ChromeDriverManager().install())

# driver = webdriver.Chrome("C:/Users/dpdnj/Downloads/chromedriver_win32/chromedriver.exe", options=chrome_options)
driver = webdriver.Chrome("C:/Users/dpdnj/Downloads/chromedriver_win32/chromedriver.exe")
url = 'https://www.musinsa.com/app/goods/996177'
driver.get(url)
time.sleep(3)

# '스타일 후기' 클릭
key = driver.find_element_by_css_selector('#estimate_style').click()
time.sleep(3)

# 처음 시작할 때, 페이지 버튼
page_btn1 = ['a:nth-child(3)','a:nth-child(4)','a:nth-child(5)','a:nth-child(6)','a:nth-child(7)']
# 두번째부터, 페이지 버튼
page_btn2 = ['a:nth-child(4)','a:nth-child(5)','a:nth-child(6)','a:nth-child(7)','a.fa.fa-angle-right.paging-btn.btn.next']

review_list = []  # 리뷰 내용
sex_list = []  # 성별
height_list = []  # 키
weight_list = []  # 몸무게
size_list = []  # 사이즈
brightness_list = []  # 밝기
color_list = []  # 색감
thickness_list = []  # 두께감

cnt = 0
while cnt < 13:
    if cnt < 1:  # cnt가 0일때(처음 시작할 때), page_btn1로 실행
        for pagenum in page_btn1:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(2)

            page = driver.find_element_by_css_selector('#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > ' + str(pagenum) + '').click()
            time.sleep(2)

            for i in range(10):
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                review_all = soup.find_all('div', class_ = 'review-contents__text')
                review = review_all[i].text
                rv = re.sub('[^0-9ㄱ-ㅣ가-힣]', " ", review)

                try:
                    information_all = soup.find_all('p', class_='review-profile__body_information')
                    information = information_all[i].text.split(',')
                    sex = information[0]
                    height = information[1]
                    weight = information[2]
                except IndexError as e:
                    sex = 'NaN'
                    height = 'NaN'
                    weight = 'NaN'

                style = soup.find_all('div', class_='review-evaluation')
                size = style[i].find_all('span')[0].text
                brightness = style[i].find_all('span')[1].text
                color = style[i].find_all('span')[2].text
                thickness = style[i].find_all('span')[3].text

                review_list.append(rv)
                sex_list.append(sex)
                height_list.append(height)
                weight_list.append(weight)
                size_list.append(size)
                brightness_list.append(brightness)
                color_list.append(color)
                thickness_list.append(thickness)

    else:
        for pagenum in page_btn2:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            time.sleep(2)

            page = driver.find_element_by_css_selector('#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > ' + str(pagenum) + '').click()
            time.sleep(2)

            for i in range(10):
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                review_all = soup.find_all('div', class_ = 'review-contents__text')
                review = review_all[i].text
                rv = re.sub('[^0-9ㄱ-ㅣ가-힣]', " ", review)

                try:
                    information_all = soup.find_all('p', class_='review-profile__body_information')
                    information = information_all[i].text.split(',')
                    sex = information[0]
                    height = information[1]
                    weight = information[2]
                except IndexError as e:
                    sex = 'NaN'
                    height = 'NaN'
                    weight = 'NaN'

                style = soup.find_all('div', class_='review-evaluation')
                size = style[i].find_all('span')[0].text
                brightness = style[i].find_all('span')[1].text
                color = style[i].find_all('span')[2].text
                thickness = style[i].find_all('span')[3].text

                review_list.append(rv)
                sex_list.append(sex)
                height_list.append(height)
                weight_list.append(weight)
                size_list.append(size)
                brightness_list.append(brightness)
                color_list.append(color)
                thickness_list.append(thickness)

    cnt += 1

musinsa = pd.DataFrame({'리뷰': review_list,
                        '성별': sex_list,
                        '키': height_list,
                        '몸무게': weight_list,
                        '사이즈': size_list,
                        '밝기': brightness_list,
                        '색감': color_list,
                        '두께감': thickness_list})

musinsa.to_csv("C:/Users/dpdnj/musinsa_review/[1]릴렉스 핏 크루 넥 반팔 티셔츠 [화이트] .csv", encoding="UTF-8", index=False)
