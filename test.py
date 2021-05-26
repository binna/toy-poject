from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

# driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + parse.quote('디액트'))
driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + parse.quote('바보'))
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')
divs = soup.select('#main_pack > div')
description = False

try:
    for div in divs:
        div = div.select('div.cm_content_wrap > div.cm_content_area._scroll_mover > div > div')
        if div:
            for target in div:
                temp = target.select('div')
                for targetDiv in temp:
                    targetDescription = targetDiv.select_one('div.detail_info > div > span.desc')
                    if targetDescription:
                        description = targetDescription.text
except:
    pass

print(description)
driver.close()

