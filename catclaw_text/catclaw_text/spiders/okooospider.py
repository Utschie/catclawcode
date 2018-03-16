#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' okooospiderman的scrapy版本 '

__author__ = 'Uyschie Dym'

import scrapy
from scrapy.http import FormRequest, Request
import YDM
import random
UAcontent = urllib.request.urlopen('file:///home/jsy/Dropbox/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个

def randomdatas(filename):#把filepath传给它，它就能得到一个随机的登录账户
    User = list()
    with open('/home/jsy/Dropbox/okoookonto_new.csv',"r") as f:#打开文件,并按行读取，每行为一个列表
         reader = csv.reader(f)
         for row in reader:
             User.append(row)
    datas = {
    'UserName':'',
    'PassWord':'',
    'LoginType':'okooo',
    'RememberMe':'1',
    'AuthType':'okooo',
    'AuthCode':'',
    }#datas的值取决于yundama
    suiji = random.randint(0,len(User)-1)
    datas['UserName'] = User[suiji][0]
    datas['PassWord'] = User[suiji][1]
    datas['AuthCode'] = ydm(filename)#验证码用云打码模块识别
    return datas

def ydm(filename):#把filepath传给它，他就能得到验证码的验证结果
    username = '921202jsy'
    password  = '921202jay'
    appid = 1
    appkey = '22cc5376925e9387a23cf797cb9ba745'
    yundama = YDM.YDMHttp(username,password,appid,appkey)
    cid, result = yundama.decode(filename, 1005, 60)
    return result


class okooospider(scrapy.Spider):

    def start_request(self):#从http://www.okooo.com/jingcai/开启会话，并获得验证码保存到本地
        url = 'http://www.okooo.com/jingcai/'
        yield scrapy.Request(url=url, callback=self.login)

    def yanzhengma(self, response):#请求验证码
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
        header['User-Agent'] = random.choice(UAlist)
        request = Request(url='http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers=header,callback=self.login)
        request.meta = {'dont_redirect'=True,
                        'download_timeout'=31
                        'dont_obey_robotstxt'=True
                        }
        yield request

    def login(self,response):
        filepath = '/home/jsy/screenshot/yanzhengma.png'
        with open(filepath,"wb") as f:
            f.write(yanzhengma.content)#保存验证码到本地
        print('已获得验证码')
        datas = randomdatas(filepath)
