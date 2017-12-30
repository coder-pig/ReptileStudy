import re
import urllib.request
from urllib.error import URLError, HTTPError

# 简单版刷阅读量的脚本
import os

blog_url = "http://blog.csdn.net/coder_pig/article/details/78868926"
ip_file = "output/xc_proxy_ip.txt"
patten = re.compile(r'^(.*)-(.*)$')
read_count = 0  # 访问次数


# 读取代理ip文件生成列表返回
def load_ip_from_file(filename):
    ip_list = []
    with open(filename, "r+") as f:
        for ip in f:
            ip_list.append(ip.replace("\n", ""))
    return ip_list


# 验证代理是否可用
def read_csdn(str_ip):
    result = patten.match(str_ip)
    ip = result.group(1)
    ip_type = result.group(2).casefold()
    proxy = {ip_type: ip}
    # 一般都可能需要请求头
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (X11; Linux x86_64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/63.0.3239.84 Safari/537.36',
        'Host': 'blog.csdn.net',
    }
    try:
        handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(handler)
        urllib.request.install_opener(opener)
        req = urllib.request.Request(blog_url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=15)
        if resp.getcode() == 200:
            global read_count
            read_count += 1
            print("累计访问成功次数： %d" % read_count)
    except (HTTPError, URLError, ConnectionResetError, Exception) as reason:
        pass
        # print(str(reason))


if not os.path.exists("output"):
    os.mkdir("output")
ip_list = load_ip_from_file(ip_file)
for ip in ip_list:
    read_csdn(ip)
