import requests
import feedparser
import os
from bs4 import BeautifulSoup as BS
import urllib.parse


# page = requests.get("https://vnexpress.net/tin-tuc/the-gioi/phan-tich/chien-tranh-thuong-mai-my-trung-cuong-quoc-dau-nhau-the-gioi-huong-loi-3822431.html")
# page = requests.get("https://dantri.com.vn/xa-hoi/can-canh-khu-dat-du-an-nha-hat-1500-ty-o-thu-thiem-20181011092114449.htm")
# print(page.status_code)
# print(page.content)
# soup = BS(page.content, "html.parser")
# print(soup.prettify())

# print("".join([s.get_text() for s in soup.find_all('p', class_='Normal')]).replace("\n", " "))
# print("".join([s.get_text() for s in soup.find(id="divNewsContent").find_all("p")[:-1]]).replace("\n", " "))


def crawVnxpress(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(link, ": Failse!")
        return ""

    soup = BS(page.content, "html.parser")
    if soup.find('p', class_="Normal") == None:
        return ""
    return "".join([s.get_text() for s in soup.find_all('p', class_="Normal")]).replace("\n", " ")


def crawDantri(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(link, ": Failse!")
        return ""

    soup = BS(page.content, "html.parser")
    return "".join([s.get_text() for s in soup.find(id="divNewsContent").find_all("p")[:-1]]).replace("\n", " ")


def crawThanhnien(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(link, ": Failse!")
        return ""

    soup = BS(page.content, "html.parser")
    return "".join([s.get_text() for s in soup.find(id="abody").find_all('div')[:-1]]).replace("\n", " ")


# Rss cho cac labels
thoi_su = ["https://vnexpress.net/rss/thoi-su.rss"]
the_gioi = []
kinh_doanh = []
startup = []
giai_tri = []
the_thao = []
phap_luat = []
giao_duc = []
truyen_cuoi = []
suc_khoe = []
doi_song = []
tam_su = []
khoa_hoc = []
xe = []
rss = {"thoi_su": thoi_su, "the_gioi": the_gioi, "kinh_doanh": kinh_doanh,
       "startup": startup, "giai_tri": giai_tri, "tam_su": tam_su, "khoa_hoc": khoa_hoc,
       "xe": xe, "the_thao": the_thao, "phap_luat": phap_luat, "giao_duc": giao_duc,
       "truyen_cuoi": truyen_cuoi, "suc_khoe": suc_khoe, "doi_song": doi_song}

print("Number of classes: ", len(rss))


# Posts info: list dict: {owner, link, class}


def getdatafrom(hostname, link):
    switcher = {
        "dantri.com.vn": crawDantri,
        'vnexpress.net': crawVnxpress,
        "thanhnien.vn": crawThanhnien
    }

    return switcher[hostname](link)


count = 0
for k_class, v_rsses in rss.items():
    if not os.path.isdir(os.getcwd() + "/data/" + k_class):
        os.makedirs(os.getcwd() + "/data/" + k_class)
    for rss_c in v_rsses:

        hostname = urllib.parse.urlparse(rss_c).hostname
        feed = feedparser.parse(rss_c)
        # posts_content = []
        for post in feed.entries:
            post_content = getdatafrom(hostname, post.link)
            if post_content == "":
                continue
            count += 1
            print(post.link)
            print(post_content)
            print("==================================")

print("Number of post: ", count)
