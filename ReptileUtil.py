# 基本爬虫常用的工具方法
import urllib
import urllib.request
import json
import urllib.parse
from http import cookiejar


# 把列表写入文件中
def write_list_to_file(filename, data_list):
    try:
        with open(filename, "w+") as f:
            for data in data_list:
                f.write(filename + "\n")
    except OSError as reason:
        print(str(reason))


# 读取列表文件返回列表
def read_list_from_file(filename):
    data_list = []
    try:
        with open(filename, "r+") as f:
            for data in f:
                data_list.append(data)
    except OSError as reason:
        print(str(reason))
    return data_list


# 1.获取网页信息
def fetch_html_body(url):
    resp = urllib.request.urlopen(url)
    data = resp.read()
    data = data.decode('utf-8')
    print(data)


# 2.下载图片
def download_pic(url):
    resp = urllib.request.urlopen(url)
    pic = resp.read()
    try:
        pic_name = url.split("/")[-1]
        with open(pic_name, "wb") as f:
            f.write(pic)
    except (OSError, Exception) as reason:
        print(str(reason))


# 3.调用urlretrieve下载音频
def download_music(url):
    music_name = url.split("/")[-1]
    urllib.request.urlretrieve(url, music_name)


# 4.模拟Get请求示例
def simulation_get():
    url = "http://gank.io/api/data/" + urllib.request.quote("福利") + "/10/1"
    resp = urllib.request.urlopen(url)
    result = json.loads(resp.read().decode('utf-8'))
    json_result = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
    print(json_result)


# 5.模拟Post请求示例
def simulation_post():
    post_url = "http://xxx.xxx.login"
    phone = "13555555555"
    password = "111111"
    values = {
        'phone': phone,
        'password': password
    }
    data = urllib.parse.urlencode(values).encode(encoding='utf-8')
    req = urllib.request.Request(post_url, data)
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())  # Byte结果转Json
    json_result = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)
    print(json_result)


# 6.修改请求头示例
def change_headers(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/63.0.3239.84 Safari/537.36',
               'Referer': 'http://www.baidu.com'}
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=20)
    print(resp.read().decode('gbk'))


# 7.使用ip代理(ip_type为代理类型，比如http,https)
def use_proxy(url, ip_type, ip):
    # 1.创建代理处理器，ProxyHandler参数是一个字典{类型:代理ip:端口}
    proxy_support = urllib.request.ProxyHandler({ip_type: ip})
    # 2.定制，创建一个opener
    opener = urllib.request.build_opener(proxy_support)
    # 3.安装opener
    urllib.request.install_opener(opener)


# 8.获得Cookie获取
def get_cookie(url):
    # 1.实例化CookieJar对象
    cookie = cookiejar.CookieJar()
    # 2.创建Cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    # 3.通过CookieHandler创建opener
    opener = urllib.request.build_opener(handler)
    # 4.打开网页
    resp = opener.open("url")
    # 5.打印Cookie
    for i in cookie:
        print("Name = %s" % i.name)
        print("Name = %s" % i.value)
    # 6.打印Cookie到文件
    cookie_file = "cookie.txt"
    cookie = cookiejar.MozillaCookieJar(cookie_file)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    resp = opener.open("http://www.baidu.com")
    cookie.save(ignore_discard=True, ignore_expires=True)
    # 7.从文件中获取Cookie并访问
    cookie_file = "cookie.txt"
    cookie = cookiejar.MozillaCookieJar(cookie_file)
    cookie.load(cookie_file, ignore_expires=True, ignore_discard=True)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    resp = opener.open("http://www.baidu.com")
    print(resp.read().decode('utf-8'))


if __name__ == '__main__':
    pass
# fetch_html_body('http://www.baidu.com')
# download_pic('https://www.baidu.com/img/bd_logo1.png')
# download_music('https://filecdn.xinli001.com/mp3/20171228/224944767.mp3')
# simulation_get()
# simulation_post()
# change_headers('http://www.biqukan.com/1_1496/')
