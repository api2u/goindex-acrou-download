import json
import requests
from urllib.parse import urlparse
from urllib.parse import unquote
import aria2c

#定义基本信息
#网址
weburl = ""
aria2host="127.0.0.1"
aria2port="6800"
downloadpath =r'D:/up'
#aria2密码
aria2session= None
#aria有密码  #aria2session= '1'   密码为空   aria2session= None
#使用代理获取下载地址
proxies = { "http": "socks5://127.0.0.1:10900",'https': 'socks5://127.0.0.1:10900'}

#递归遍历目录
def ListGoindex(url):
    #设置请求参数
    d = json.dumps({
    'page_index': 0
    })
    headers = {'Content-Type': 'application/json','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    #发送请求
    res = requests.post(url=url,data=d,headers=headers,proxies=proxies)
    #处理返回结果
    res=json.loads(res.text)["data"]["files"]
    #循环取出结果
    for item in res:
        #判断是目录递归
        if item["mimeType"] == 'application/vnd.google-apps.folder':
            #取出子路径
            tmp=url+item["name"]+'/'
            ListGoindex(tmp)
        else:
            #添加到下载器
            FileDownload(url+item["name"])

def FileDownload(url):
    #使用的下载器
    aria2(url)

print("第一次使用请打开文件配置aria2参数")
print("正在测试aria2链接情况，下面输出aria2版本号即为成功")
aria2 = aria2c.Aria2c(host=aria2host, port=aria2port,token=aria2session)
print("aria2版本号为:"+aria2.getVer())
print("-------------------------")

def aria2(url):
    tmp=urlparse(url.replace('/'+url.split('/')[-1],''))
    tmp=unquote(tmp.path, encoding="utf-8").replace('/0:','')
    options = {"dir": downloadpath+tmp}
    aria2 = aria2c.Aria2c(host=aria2host, port=aria2port,token=aria2session)
    aria2.addUri(url,options=options)

weburl = input("请输入goindex-theme-acrou的网址:\n")
ListGoindex(weburl)

print("提交成功")