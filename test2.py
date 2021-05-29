from selenium import webdriver
from bs4 import BeautifulSoup
from flask import Flask, render_template, request,jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

app = Flask(__name__)

driver = webdriver.Chrome('/Users/jinwoojung/Downloads/chromedriver')
# driver = webdriver.Chrome('./chromedriver')

driver.implicitly_wait(3)


def check_watcha():
    url2 = 'https://watcha.com/staffmades/3260'
    driver.get(url2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select('#root > div.css-urf8br-Self.e19xg79h0 > main > div > section > ul > li')
    for title in titles:
        name2 = title.select_one('li > div > ul')
        try:
            for name in name2:
                title = name.select_one('li > div > div.css-1g3awd').text
                driver.get('https://www.google.com/search?q=영화 ' + title)
                req = driver.page_source
                soup = BeautifulSoup(req, 'html.parser')
                tag = soup.select('div.SPZz6b > h2')
                if title == '이멜다 마르코스: 사랑의 영부인' or title == '상어' or title == '가짜사나이 2: 더 메이킹':
                    doc = {
                        'name': 'watcha',
                        'title': title,
                        'div': 'movie'
                    }
                    print(doc)
                elif tag == [] or title == '우주전쟁' or title == '코요테' or title =='네메시스':
                    doc = {
                        'name': 'watcha',
                        'title': title,
                        'div': 'drama'
                    }
                    print(doc)
                else:
                    doc = {
                        'name': 'watcha',
                        'title': title,
                        'div': 'movie'
                    }
                    print(doc)
        except:
            continue

        # 안맞는 리스트
        # 우주전쟁 드라마
        # 네메시스 드라마
        # 코요테 드라마
        # 이멜다 마르코스 영화
        # 상어 영화
        # 가짜사나이 2 영화



check_watcha()


driver.close()



