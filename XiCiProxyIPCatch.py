# 抓取西刺高匿代理ip

import urllib.request
from urllib.error import URLError, HTTPError
import os
from bs4 import BeautifulSoup
import random
import time

xc_proxy_ip_url = "http://www.xicidaili.com/nn/"  # 抓取源
xc_proxy_ip_file = "output/xc_proxy_ip.txt"  # 代理ip存放文件
begin_page = 1  # 抓取的起始页
end_page = 1000  # 抓取的最后一页


# 把ip列表写入到文件中
def write_ip_to_file(ip_list):
    try:
        with open(xc_proxy_ip_file, "a+") as f:
            for ip in ip_list:
                f.write(ip + "\n")
    except OSError as reason:
        print(str(reason))


# 抓取网页里的ip，端口与类型
def catch_ip_form_page(page_url):
    print("开始抓取：" + page_url)
    ip_list = []
    headers = {
        'Host': 'www.xicidaili.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    try:
        # 随缘休息，避免访问过于频繁被锁ip
        sleep_time = random.randint(10, 20)
        time.sleep(sleep_time)
        # 访问西刺
        req = urllib.request.Request(page_url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=20)
        content = resp.read()
        soup = BeautifulSoup(content, 'html.parser')
        catch_list = soup.find_all('tr')[1:]
        for tr in catch_list:
            td = tr.find_all('td')
            ip_list.append(td[1].get_text() + ":" + td[2].get_text() + "-" + td[5].get_text())
    except (HTTPError, URLError, ConnectionResetError, Exception) as reason:
        print(str(reason))
        pass
    return ip_list


if __name__ == '__main__':
    if not os.path.exists("output"):
        os.mkdir("output")
    if os.path.exists(xc_proxy_ip_file):
        os.remove(xc_proxy_ip_file)
    for i in range(begin_page, end_page + 1):
        url = xc_proxy_ip_url + str(i)
        result_list = catch_ip_form_page(url)
        write_ip_to_file(result_list)
