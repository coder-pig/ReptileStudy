# 抓取比去看笔趣看小说网站的小说

from bs4 import BeautifulSoup
import urllib.request
from urllib import error
import os.path

novel_url = "http://www.biqukan.com/1_1496/"  # 小说页面地址
base_url = "http://www.biqukan.com"  # 根地址，用于拼接
save_dir = "output/Novel/"  # 下载小说的存放路径


# 保存小说到本地
def save_chapter(txt, path):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    try:
        with open(path, "a+") as f:
            f.write(txt.get_text(strip=True))
    except (error.HTTPError, OSError) as reason:
        print(str(reason))
    else:
        print("下载完成：" + path)


# 获得所有章节的url
def get_chapter_url():
    chapter_req = urllib.request.Request(novel_url)
    chapter_resp = urllib.request.urlopen(chapter_req, timeout=20)
    chapter_content = chapter_resp.read()
    chapter_soup = BeautifulSoup(chapter_content, 'html.parser')
    # 取出章节部分
    listmain = chapter_soup.find_all(attrs={'class': 'listmain'})
    a_list = []  # 存放小说所有的a标签
    # 过滤掉不是a标签的数据
    for i in listmain:
        if 'a' not in str(i):
            continue
        for d in i.findAll('a'):
            a_list.append(d)
    # 过滤掉前面"最新章节列表"部分
    result_list = a_list[12:]
    return result_list


# 获取章节内容并下载
def get_chapter_content(c):
    chapter_url = base_url + c.attrs.get('href')  # 获取url
    chapter_name = c.string  # 获取章节名称
    chapter_req = urllib.request.Request(chapter_url)
    chapter_resp = urllib.request.urlopen(chapter_req, timeout=20)
    chapter_content = chapter_resp.read()
    chapter_soup = BeautifulSoup(chapter_content, 'html.parser')
    # 查找章节部分内容
    showtxt = chapter_soup.find_all(attrs={'class': 'showtxt'})
    for txt in showtxt:
        save_chapter(txt, save_dir + chapter_name + ".txt")


if __name__ == '__main__':
    novel_list = get_chapter_url()
    for chapter in novel_list:
        get_chapter_content(chapter)
