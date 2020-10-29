import os
import time

import requests
from bs4 import BeautifulSoup
import re


def search(name):
    response = requests.get("http://www.uutu.me/index.php?c=Search&keyword={}".format(name))
    soup = BeautifulSoup(response.content, "lxml")
    return name, soup


def find_you_want(soup):
    dic = {}
    div = soup.find_all("div", class_="thumbnail")
    for i in div:
        href = i.a["href"]
        girl_name = i.a.img["alt"]
        # print(href,girl_name)
        dic[girl_name]=href
    return dic


def make_2_dir(name, girl_name):
    try:
        if os.path.exists("../{}".format(name)):
            if os.path.exists("../{}/{}".format(name, girl_name)):
                pass
            else:
                os.mkdir("../{}/{}".format(name, girl_name))
                print("正在创建二级目录{}".format(girl_name))
        else:
            os.mkdir("../{}".format(name))
            print("正在创建一级目录{}".format(name))

        return "../{}/{}".format(name, girl_name)
    except Exception as e:
        print("创建目录失败")


def girl_page(href):
    print("搜索网址中...")
    page_list = []
    response = requests.get(href)
    soup = BeautifulSoup(response.content,"lxml")
    div = soup.find("div", class_="page-show")
    a = div.find_all("a")
    num = a[-2].text
    for i in range(1,int(num)+1):
        if i==1:
            page_list.append(href)
        else:
            page_list.append(href+"&p={}".format(i))
    print("搜索到{}个网页。".format(len(page_list)))
    return page_list


def pp(page_list):
    print("搜索图片中...")
    jpg = []
    for url in page_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content,"lxml")
        img = soup.find("img", class_="img-responsive")
        jpg.append(img["src"])
    print("搜索到{}张图片。".format(len(jpg)))
    return jpg



def get_picture(path,page_list):
    a = 0
    for url in page_list:
        response = requests.get(url)
        path1 = path+"/{}.jpg".format(a)
        with open(path1,"wb") as f:
            f.write(response.content)
        print("-----------------"+path1+"下载完成"+"-----------------------")
        a+=1


def go():
    user = input("请输入妹子类型：")
    name, soup = search(user)
    dic= find_you_want(soup)
    for girl_name in dic.keys():
        path = make_2_dir(name,girl_name)
        page_list = girl_page(dic[girl_name])
        jpg = pp(page_list)
        get_picture(path,jpg)

if __name__ == '__main__':
    go()

