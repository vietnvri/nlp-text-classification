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
        print(link, "khong chua the Mormal")
        return ""
    return "".join([s.get_text() for s in soup.find_all('p', class_="Normal")]).replace("\n", " ")


def crawDantri(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(link, ": Failse!")
        return ""

    soup = BS(page.content, "html.parser")
    if soup.find(id="divNewsContent") == None:
        print(link, "khong chua the divNewsContent")
        return ""
    return "".join([s.get_text() for s in soup.find(id="divNewsContent").find_all("p")[:-1]]).replace("\n", " ")


def crawThanhnien(link):
    page = requests.get(link)
    if page.status_code != 200:
        print(link, ": Failse!")
        return ""

    soup = BS(page.content, "html.parser")
    if soup.find(id="abody") == None:
        print(link, "khong chua the abody")
        return ""
    return "".join([s.get_text() for s in soup.find(id="abody").find_all('div')]).replace("\n", " ")


# Rss cho cac labels
# thoi_su = ["https://vnexpress.net/rss/thoi-su.rss", "https://thanhnien.vn/rss/viet-nam.rss"]
kinh_doanh = ["https://dantri.com.vn/kinh-doanh.rss", "https://thanhnien.vn/rss/kinh-doanh.rss",
              "https://vnexpress.net/rss/kinh-doanh.rss", "https://vnexpress.net/rss/startup.rss"]
the_gioi = ["https://dantri.com.vn/the-gioi.rss", "https://thanhnien.vn/rss/the-gioi.rss",
            "https://vnexpress.net/rss/the-gioi.rss"]
giai_tri = ["https://dantri.com.vn/giai-tri.rss", "https://thanhnien.vn/rss/ban-can-biet/giai-tri.rss",
            "https://vnexpress.net/rss/giai-tri.rss"]
the_thao = ["https://dantri.com.vn/the-thao.rss", "https://thethao.thanhnien.vn/rss/home.rss",
            "https://vnexpress.net/rss/the-thao.rss"]
phap_luat = ["https://dantri.com.vn/phap-luat.rss", "https://thanhnien.vn/rss/viet-nam/phap-luat.rss",
             "https://vnexpress.net/rss/phap-luat.rss"]
giao_duc = ["https://dantri.com.vn/giao-duc-khuyen-hoc.rss", "https://thanhnien.vn/rss/giao-duc.rss",
            "https://vnexpress.net/rss/giao-duc.rss"]
suc_khoe = ["https://dantri.com.vn/suc-khoe.rss", "https://thanhnien.vn/rss/doi-song/suc-khoe.rss",
            "https://vnexpress.net/rss/suc-khoe.rss"]
van_hoa = ["https://dantri.com.vn/van-hoa.rss", "https://thanhnien.vn/rss/van-hoa-nghe-thuat.rss"]
khoa_hoc = ["https://dantri.com.vn/khoa-hoc-cong-nghe.rss", "https://vnexpress.net/rss/khoa-hoc.rss"]
xe = ["https://dantri.com.vn/o-to-xe-may.rss", "https://xe.thanhnien.vn/rss/home.rss",
      "https://vnexpress.net/rss/oto-xe-may.rss"]

rss = {"the_gioi": the_gioi, "kinh_doanh": kinh_doanh,
       "giai_tri": giai_tri, "khoa_hoc": khoa_hoc,
       "xe": xe, "the_thao": the_thao, "phap_luat": phap_luat, "giao_duc": giao_duc,
       "suc_khoe": suc_khoe, "van_hoa": van_hoa}

print("Number of classes: ", len(rss))


# Posts info: list dict: {owner, link, class}


def getdatafrom(hostname, link):
    switcher = {
        "dantri.com.vn": crawDantri,
        'vnexpress.net': crawVnxpress,
        "thanhnien.vn": crawThanhnien
    }
    if "dantri.com.vn" in hostname:
        return switcher["dantri.com.vn"](link)
    elif "vnexpress.net" in hostname:
        return switcher["vnexpress.net"](link)
    else:
        return switcher["thanhnien.vn"](link)


def saveFile(content, path):
    # check file exist
    if os.path.isfile(path):
        return
    file = open(path, "w")
    file.write(content)
    file.close()


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

            saveFile(post_content, os.getcwd() + "/data/" + k_class + "/" + post.link.split("/")[-1])
            print(post.link.split("/")[-1])
            print(post_content)
            print("==================================")

print("Number of post: ", count)
