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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'")
chrome_options.add_experimental_option("detach", True)

chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# service = Service(executable_path=ChromeDriverManager().install())

# driver = webdriver.Chrome("C:/Users/dpdnj/Downloads/chromedriver_win32/chromedriver.exe", options=chrome_options)
driver = webdriver.Chrome("C:/Users/dpdnj/Downloads/chromedriver_win32/chromedriver.exe")
url = 'https://www.musinsa.com/app/goods/947067'
driver.get(url)
time.sleep(3)

key = driver.find_element_by_css_selector('#estimate_style').click()
time.sleep(3)

page_btn = ['a:nth-child(4)','a:nth-child(5)','a:nth-child(6)','a:nth-child(7)','a.fa.fa-angle-right.paging-btn.btn.next']
review_list = []

cnt = 0
while cnt < 13:
    for pagenum in page_btn:

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(3)

        page = driver.find_element_by_css_selector('#reviewListFragment > div.nslist_bottom > div.pagination.textRight > div > ' + str(pagenum) + '').click()
        time.sleep(3)

        for i in range(10):
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            review_all = soup.find_all('div', class_ = 'review-contents__text')
            review = review_all[i].text
            rv = re.sub('[^0-9ㄱ-ㅣ가-힣]', " ", review)
            review_list.append(rv)
    
    cnt += 1

# with open("C:/Users/dpdnj/musinsa_review/musinsa_rank1.csv", "w", encoding="UTF-8", newline="") as file:
#     writer = csv.writer(file)
#     for i in review_list:
#         writer.writerow(i)

musinsa = pd.DataFrame({'Review':review_list})
musinsa.to_csv("C:/Users/dpdnj/musinsa_review/[5]스웨트 셔츠[블랙].csv", encoding="UTF-8", index=False)