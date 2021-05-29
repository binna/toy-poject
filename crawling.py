from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.toyProject

# driver = webdriver.Chrome('/Users/jinwoojung/Downloads/chromedriver')
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)


def search_naver_description(name):
    driver.get(
        'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + name.replace("[스페셜]", ""))
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


def watcha(url, name):
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    lis = soup.select('#root > div.css-1v324cc-Self.e19xg79h0 > main > div > section > ul > li')

    for targetLi in lis:
        li = targetLi.select('div.css-pge0c7-Row > ul > li')
        for target in li:
            title = target.select_one(' div > div.css-1g3awd > div > div').text
            description = search_naver_description(title)
            try:
                img = target.select_one(
                    'li > div > div.css-cssveg > div.css-omgs1s > div.css-fcehsw-StyledSelf.e1q5rx9q0 > span').attrs[
                    'style'].replace("background-image: url(\"", "").replace("\");", "")
            except:
                doc = {
                    'name': name,
                    'title': title,
                    'image': img,
                    'desc': description
                }
                db.watcha.insert_one(doc)
                continue
            doc = {
                'name': name,
                'title': title,
                'image': img,
                'desc': description
            }
            db.watcha.insert_one(doc)


def wavve(url, name):
    driver.get(url)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    titles = soup.select('#g-contents > div.list-view-detail > div')
    for target in titles:
        title = target.select_one('a > div.sub-title > div > div > span').text
        targetImg = target.select_one('a > div.thumb-image > img')
        img = targetImg.attrs['data-src']
        driver.get('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + title)
        description = search_naver_description(title)
        doc = {
            'name': name,
            'title': title,
            'image': img,
            'desc': description
        }
        db.wavve.insert_one(doc)


def server_restart():
    db.wavve.drop()
    db.watcha.drop()

    # TODO 회의를 통해 영화부분을 예능으로 바꿀지 협의
    wavve(
        'https://www.wavve.com/list/EN20392?api=apis.wavve.com%252Fcf%252Fthemes%252F20392%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN20392%2526uiparent%253DGN59-EN20392%2526uirank%253D9%2526broadcastid%253DGN59_EN20392_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN20392%2526mtype%253Dsvod&came=BandViewGnbCode',
        'movie')

    wavve(
        'https://www.wavve.com/list/EN397?api=apis.wavve.com%252Fcf%252Fthemes%252F397%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN397%2526uiparent%253DGN13-EN397%2526uirank%253D1%2526broadcastid%253DGN13_EN397_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN397&came=BandViewGnbCode&page=1',
        'drama')
    wavve(
        'https://www.wavve.com/list/EN397?api=apis.wavve.com%252Fcf%252Fthemes%252F397%253Fcontenttype%253Dx%2526WeekDay%253Dall%2526uitype%253DEN397%2526uiparent%253DGN13-EN397%2526uirank%253D1%2526broadcastid%253DGN13_EN397_pc_none_none%2526offset%253D0%2526limit%253D20%2526uicode%253DEN397&came=BandViewGnbCode&page=2',
        'drama')

    # TODO 회의를 통해 영화부분을 예능으로 바꿀지 협의
    watcha('https://watcha.com/explore?genre=368', 'movie')  # 재난
    watcha('https://watcha.com/explore?genre=260635', 'movie')  # 로멘틱 코미디
    watcha('https://watcha.com/explore?genre=371', 'movie')  # 시대극
    watcha('https://watcha.com/explore?genre=487576', 'movie')  # SF

    watcha('https://watcha.com/explore?genre=353', 'drama')  # 드라마
    driver.close()
