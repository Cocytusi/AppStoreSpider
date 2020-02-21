import urllib.request
import math
from urllib.parse import quote
from lxml import etree
import re
import requests


class Spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
        }
        self.url = 'http://appstore.huawei.com/search/'
        self.AppList = ['物联网'] #'物联','iot','IOT','智能','家居',,'link','音箱','摄像头','smart'
    def searchApp(self):
        SearchLink_list = []

        for AppName in self.AppList:
            p = self.pages(self.url + quote(AppName))
            for i in range(1,p+1):
                SearchLink = self.url + quote(AppName) + '/' + str(i)
                SearchLink_list.append(SearchLink)

        print(SearchLink_list)
        self.loadPage(SearchLink_list)
    def loadPage(self, UrlList):
        for url in UrlList:
            req = urllib.request.Request(url, headers=self.headers)
            html = urllib.request.urlopen(req).read().decode('utf-8')
            content = etree.HTML(html)

            for i in range(2,24):

                xpath = '//*/div[1]/div[4]/div[1]/div/div/div['+str(i)+']/div[2]/div[2]/a/@onclick'
                down = content.xpath(xpath) # 获取下载链接存放的标签，
            # 返回的是一大堆乱七八糟
                p = re.compile(r'[(](.*?)[)]', re.S)
                appInfo = re.findall(p, down[0])[0]
                appInfo = tuple(eval(appInfo)) # 将获取的APP信息存入元祖
                print("该页面第" + str(i-1) + "个apk")
                print("正在爬取%s" % appInfo[1] + appInfo[6])
            # print(appInfo[6]) # 下载链接
                self.downLoad(appInfo[1], appInfo[6],appInfo[5])
    def downLoad(self, name, version,link):
        PackageName = 'D:/123/save/' + name + '_' + version + '.apk'
        App = requests.get(link)
        AppInfo = App.content
        with open(PackageName, 'wb') as f:
            f.write(AppInfo)
        print('%s爬取完成' % name + version)

    def pages(self,url):
        req = urllib.request.Request(url, headers=self.headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        content = etree.HTML(html)
        down = content.xpath('//*/div[1]/div[4]/div[1]/div[1]/div[1]/div[1]/p/span/span')  # 获取下载总页数
        p = re.compile(r'\d+', re.S)
        appInfo = re.findall(p, down[0].text)
        s = math.floor(int(appInfo[0])/24)
        return s

if __name__ == '__main__':
    spd = Spider()
    spd.searchApp()

