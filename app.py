import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

# driver = webdriver.Chrome('절대값 주소')
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

app = Flask(__name__)


def crawling_wavve():
    doc = {'wavve': []}
    a = [1, 2]
    for b in a:
        url = 'https://www.wavve.com/list/EN397?api=apis.wavve.com%252Fcf%252Fthemes%252F397%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN397%2526uiparent%253DGN13-EN397%2526uirank%253D1%2526broadcastid%253DGN13_EN397_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN397&came=BandViewGnbCode&page=' + str(
            b)
        driver.get(url)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        titles = soup.select('#g-contents > div.list-view-detail > div')
        for title in titles:
            name = title.select_one('a > div.sub-title > div > div > span').text
            img = title.select_one('a > div.thumb-image > img')
            img2 = img.attrs['data-src']
            driver.get(
                'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + name.replace(
                    "[스페셜]", ""))
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            divs = soup.select('#main_pack > div')
            description = False
            try:
                for div in divs:
                    div = div.select('div.cm_content_wrap > div > div > div')
                    if div:
                        for target in div:
                            temp = target.select('div')
                            for targetDiv in temp:
                                targetDescription = targetDiv.select_one('div.detail_info > div > span.desc')
                                if targetDescription:
                                    description = targetDescription.text
            except:
                pass
            doc['wavve'].append({
                'title': name,
                'image': img2,
                'desc': description
            })
    # print(doc)
    return jsonify(doc)


def crawling_watcha():
    url2 = 'https://watcha.com/staffmades/3260'
    driver.get(url2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select('#root > div.css-urf8br-Self.e19xg79h0 > main > div > section > ul > li')
    doc = {'watcha': []}

    for title in titles:
        name2 = title.select_one('li > div > ul')
        for name in name2:
            title = name.select_one('li > div > div.css-1g3awd').text
            driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + title)
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')
            divs = soup.select('#main_pack > div')
            description = False
            try:
                for div in divs:
                    div = div.select('div.cm_content_wrap > div > div > div')
                    if div:
                        for target in div:
                            temp = target.select('div')
                            for targetDiv in temp:
                                targetDescription = targetDiv.select_one('div.detail_info > div > span.desc')
                                if targetDescription:
                                    description = targetDescription.text
            except:
                pass
            try:
                img = name.select_one(
                    'li > div > div.css-cssveg > div.css-omgs1s > div.css-fcehsw-StyledSelf.e1q5rx9q0 > span').attrs[
                    'style'].replace("background-image: url(\"", "").replace("\");", "")
            except:
                doc['watcha'].append({
                    'title': title,
                    'image': img,
                })
                continue

            doc['watcha'].append({
                'title': title,
                'image': img,
                'desc': description
            })
    # print(doc)
    return jsonify(doc)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    # app.run('0.0.0.0', port=5000, debug=True)
    crawling_wavve()
    # crawling_watcha()

    driver.close()
