import requests
import urllib.request
import re
import os

from urllib import robotparser
from collections import deque
from bs4 import BeautifulSoup

rp = robotparser.RobotFileParser()

def check_robot_txt(url):
    rp.set_url((url + "/robots.txt"))
    rp.read()
    return rp.can_fetch("*",url)

def explore_links(url):
    link_list = []
    url_file = urllib.request.urlopen(url)
    url_content = url_file.read()
    url_file.close()

    soup = BeautifulSoup(url_content,features="lxml")
    for links in soup.find_all("a", href = re.compile("http://")):
        link_list.append(links.get("href"))
    return link_list

def BrFS_crawler(url, max_count):
    visited, queue, count = set(), deque(), 1
    queue.append(url) #begining of the search
    while queue and count < max_count + 1:
        url = queue.popleft() #extract one element from the left

        if url in visited:
            continue #skip url
        if check_robot_txt(url) is not True:
            continue #skip url

        visited.add(url)
        queue.extend(explore_links(url))
        print("[%s] %s"%(count,url))
        r = requests.get(url)
        try:
            with open("html_files/file [%s].html"%(count),"w") as file:
                file.write(r.text)
            count += 1
        except:
            count +=1
            continue


if __name__ == '__main__':
    url = "http://" + input("input a URL (example: www.upf.com) ---> ")
    max_count= int(input("how many links would you like to include on the search?: "))
    check_robot_txt(url)
    BrFS_crawler(url,max_count)