from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.toyProject

# driver = webdriver.Chrome('/Users/jinwoojung/Downloads/chromedriver')
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)


def search_naver_description(name):
    driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + name.replace("[스페셜]", ""))
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    divs = soup.select('#main_pack > div')
    try:
        for div in divs:
            div = div.select('div.cm_content_wrap > div > div > div')
            if div:
                for target in div:
                    temp = target.select('div')
                    for targetDiv in temp:
                        targetDescription = targetDiv.select_one('div.detail_info > div > span.desc')
                        if targetDescription:
                            return targetDescription.text
    except:
        return False


def wavve_movie():
    url = 'https://www.wavve.com/list/EN20392?api=apis.wavve.com%252Fcf%252Fthemes%252F20392%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN20392%2526uiparent%253DGN59-EN20392%2526uirank%253D9%2526broadcastid%253DGN59_EN20392_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN20392%2526mtype%253Dsvod&came=BandViewGnbCode'
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select('#g-contents > div.list-view-detail > div')
    for title in titles:
        name = title.select_one('a > div.sub-title > div > div > span').text
        targetImg = title.select_one('a > div.thumb-image > img')
        img = targetImg.attrs['data-src']
        driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + name)
        description = search_naver_description(name)
        doc = {
            'name': 'movie',
            'title': name,
            'image': img,
            'desc': description
        }
        db.wavve.insert_one(doc)


def wavve_drama():
    a = [1, 2]
    for b in a:
        url = 'https://www.wavve.com/list/EN397?api=apis.wavve.com%252Fcf%252Fthemes%252F397%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN397%2526uiparent%253DGN13-EN397%2526uirank%253D1%2526broadcastid%253DGN13_EN397_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN397&came=BandViewGnbCode&page=' + str(b)
        driver.get(url)
        req = driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        titles = soup.select('#g-contents > div.list-view-detail > div')
        for title in titles:
            name = title.select_one('a > div.sub-title > div > div > span').text
            targetImg = title.select_one('a > div.thumb-image > img')
            img = targetImg.attrs['data-src']
            description = search_naver_description(name)
            doc = {
                'name': 'wavve-drama',
                'title': name,
                'image': img,
                'desc': description
            }
            db.wavve.insert_one(doc)


def watcha():
    url2 = 'https://watcha.com/staffmades/3260'
    driver.get(url2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select('#root > div.css-urf8br-Self.e19xg79h0 > main > div > section > ul > li')
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
                print('watcha ', title)
                continue
            doc = {
                'name': 'watcha',
                'title': title,
                'image': img,
                'desc': description
            }
            db.watcha.insert_one(doc)


def server_restart():
    db.wavve.drop()
    db.watcha.drop()
    wavve_movie()
    wavve_drama()
    watcha()
    driver.close()
