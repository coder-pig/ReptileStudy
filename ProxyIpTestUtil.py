# 测试代理ip对于某个网站是可用
# 采集响应时间在15s内存起来

import urllib.request
from urllib.error import URLError, HTTPError
import os
import re

proxy_ip_file = "output/xc_proxy_ip.txt"
save_file_name = "output/available_ip.txt"
test_url = "http://blog.csdn.net/"  # 需要进行测试的网站
# 用于匹配获得ip和ip类型的正则：
patten = re.compile(r'^(.*)-(.*)$')


# 读取代理ip文件生成列表返回
def load_ip_from_file(filename):
    ip_list = []
    with open(filename, "r+") as f:
        for ip in f:
            ip_list.append(ip.replace("\n", ""))
    return ip_list


# 保存可用ip到文件中
def save_ip_to_file(str_ip):
    try:
        with open(save_file_name, "a+") as f:
            f.write(str_ip + "\n")
    except OSError as reason:
        print(str(reason))


# 验证代理是否可用
def test_proxy_ip(str_ip):
    result = patten.match(str_ip)
    ip = result.group(1)
    ip_type = result.group(2).casefold()
    proxy = {ip_type: ip}
    # 一般都可能需要请求头
    headers = {
        'Host': test_url,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    try:
        handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(test_url, headers=headers)
        test_resp = urllib.request.urlopen(req, timeout=15)
        if test_resp.getcode() == 200:
            save_ip_to_file(str_ip)
    except (HTTPError, URLError, ConnectionResetError, Exception) as reason:
        print(str(reason))


if not os.path.exists("output"):
    os.mkdir("output")
ip_list = load_ip_from_file(proxy_ip_file)
for ip in ip_list:
    test_proxy_ip(ip)
