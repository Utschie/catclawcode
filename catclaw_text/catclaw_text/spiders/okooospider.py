#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#妈的怎么本来好好的就编辑器就无响应了呢？！！！艹！！！————17.03.2018
#函数scrapy_splash之前的部分经测试没有问题————24.03.2018
#决定放弃使用splash，而是直接在相应网页的ajax请求中直接得到公司列表————25.03.2018
' okooospiderman的scrapy版本 '

__author__ = 'Uyschie Dym'

import scrapy
from scrapy.http import FormRequest, Request
from catclaw_text.items import CatclawTextItem
import YDM
import random
import urllib
import re
import csv
from bs4 import BeautifulSoup#在提取代码的时候还是要用到beautifulsoup来提取标签
from datetime import datetime, timedelta, timezone#用来把时间字符串转换成时间
import pytz#用来设置时区信息
import os#用来获取文件名列表


UAcontent = urllib.request.urlopen('file:///home/jsy/Dropbox/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个


header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
header['User-Agent'] = random.choice(UAlist)
header2 = header
header2['Referer'] = 'http://www.okooo.com/soccer/'#必须加上这个才能进入足球日历
header2['Upgrade-Insecure-Requests'] = '1'#这个也得加上
meta1 = {'dont_redirect':True,
        'download_timeout':31,
        'dont_obey_robotstxt':True,
        }
meta2 = {'dont_redirect':True,
        'download_timeout':16,
        'dont_obey_robotstxt':True,
        }
meta3 = {'dont_redirect':True,
        'download_timeout':9.5,
        'dont_obey_robotstxt':True,
        }


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


def dateRange(start, end, step=1, format="%Y-%m-%d"):#生成日期的函数，得到一个生成器对象来给dangtianbisai每次调用时迭代
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    for i in range(0, days, step):
        yield strftime(strptime(start, format) + timedelta(i), format)


datelist = dateRange("2017-09-30", "2017-10-31")#datelist是一个生成器，每次调用会返回下一个日期
class okooospider(scrapy.Spider):

    def start_request(self):#从http://www.okooo.com/jingcai/开启会话，并获得验证码
        url = 'http://www.okooo.com/jingcai/'
        for i in datelist:
            request = Request(url=url,headers=header,meta=meta1,callback=self.login)
            request.meta['date'] = i
            yield request

    def yanzhengma(self, response):#请求验证码
        request = Request(url='http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers=header,meta=meta1,callback=self.login)
        request.meta['date'] = response.meta['date']
        yield request

    def login(self,response):#将得到的验证码保存并传到云打码识别，随后随机账户登录
        filepath = '/home/jsy/screenshot/yanzhengma.png'
        with open(filepath,"wb") as f:
            f.write(response.body)#保存验证码到本地
        print('已获得验证码')
        datas = randomdatas(filepath)
        print('云打码已尝试一次')
        request = FormRequest(url='http://www.okooo.com/I/?method=user.user.userlogin',formdata=datas,meta=meta2,callback=self.zuqiuzhongxin)
        request.meta['date'] = response.meta['date']
        yield request

    def zuqiuzhongxin(self,response):#登陆后进入足球中心页面
        request = Request(url='http://www.okooo.com/soccer/',headers=header,meta=meta2,callback=self.zuqiurili)
        request.meta['date'] = response.meta['date']
        yield request

    def zuqiurili(self,response):#进入足球中心后再进入足球日历
        request = Request(url='http://www.okooo.com/soccer/match/',headers=header2,meta=meta2,callback=self.dangtianbisai)
        request.meta['date'] = response.meta['date']
        yield request

    def dangtianbisai(self,response):#每次调用从datelist里取出一个日期来,进入那一天，得到当天比赛列表
        date = response.meta['date']
        request = Request(url='http://www.okooo.com/soccer/match/?date=' + date,headers=header2,callback=self.danchangbisai)
        request.meta = {'dont_redirect':True,
                        'download_timeout':31,
                        'dont_obey_robotstxt':True,
                        }
        yield request

    def danchangbisai(self,response):#从dangtianbisai的源码中获取比赛列表，并同步进行
        content1 = response.body.decode('GB18030')
        sucker1 = '/soccer/match/.*?/odds/'
        bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
        print(str(bisaiurl))
        for i in range(0.len(bisaiurl)):
            yield Request(url='http://www.okooo.com' + bisaiurl[i],headers=header2,meta=meta1,callback=self.ajax_companylist)

    def ajax_companylist(self,response):#根据每一场比赛的链接提交ajax请求，得到的response传递给einzelcompany函数
        for i in range(0,450,30):
            yield Request(url=response.url+'ajax/?page='+str(i)+'&trnum='+str(30*i)+'&companytype=BaijiaBooks&type=0',headers=header2,meta=meta1,callback=self.einzelcompany)

    def einzelcompany(self,response):#从ajax请求下来的非空源码中获取某一场里面的单个公司的链接，并提交请求,
        if len(response.text) > 163:
            sucker2 = 'href="(http://www.okooo.com/soccer/match/.*?/odds/change/.*?/)"'
            companylist = re.findall(sucker2,response.text)
            companylist = list(set(companylist))#得到了一组单个公司的链接列表
            for i in companylist:
                yield Request(url=i,headers=header2,meta=meta3,callback=self.datatopipeline)

    def datatopipeline(self,response):#单个公司页面从得到的response中提取出数据传给pipeline
        content3 = response.text.decode('gb18030')
        sucker3 = '<a class="bluetxt" href="/soccer/match/(.*?)/odds/change/(.*?)/">'
        sucker4 = '> <b>(.*?)</b>'
        sucker5 = '/schedule/">(.*?)</a>'
        sucker6 = 'odds/">(.*?) vs (.*?)</a>'
        cid = re.search(sucker3,content3).group(2)
        urlnum = re.search(sucker3,content3).group(1)
        companyname = re.search(sucker4,content3).group(1)
        league = re.search(sucker5,content3).group(1)
        zhudui = re.search(sucker6,content3).group(1)
        kedui = re.search(sucker6,content3).group(2)
        collection = db[date + '_'+ urlnum]
        soup = BeautifulSoup(content3,"lxml")
        table = soup.table
        tr = table.find_all('tr')
        del tr[0],tr[0],tr[1]
        s1 = list()
        for x in range(0,len(tr)):
            s1.append(str(tr[x]))
        sucker7 = '(>)(.*?)(<)'
        s2 = list()#s2为存储时间和赔率的列表
        for u in range(0,len(s1)):
            uu = re.findall(sucker7,s1[u])
            uuu = list()
            for w in range(0,len(uu)):
                uuu.append(uu[w][1])
            while '' in uuu:
                uuu.remove('')#去除列表中的空元素
            for i in range(0,len(uuu)):
                if uuu[i][-1] == '↑':#去除列表中的箭头们
                    uuu[i] = uuu[i][:-1]
                elif uuu[i][-1] == '↓':
                    uuu[i] = uuu[i][:-1]
            for i in range(2,len(uuu)):
                uuu[i] = float(uuu[i])
            s2.append(uuu)
        tzinfo = pytz.timezone('Etc/GMT-8')#先定义时区信息,这里代表北京时间
        for i in range(0,len(s2)):#把s2中的时间转换成UTC时间
            s2[i][0] = datetime.strptime(s2[i][0][:16],'%Y/%m/%d %H:%M')#先转成datetime实例（北京时间）
            s2[i][0] = s2[i][0].replace(tzinfo = tzinfo)#讲时间都标上北京时间
            s2[i][0] = s2[i][0].astimezone(timezone(timedelta(hours=0)))#转换成utc时间
        for i in range(0,len(s2)):#把概率转化成百分比
            s2[i][5] = round(s2[i][5]*0.01,4)#还必须得四舍五入，要不然不是两位小数
            s2[i][6] = round(s2[i][6]*0.01,4)
            s2[i][7] = round(s2[i][7]*0.01,4)
        for i in range(0,len(s2)):#把剩余时间转化成分钟数
            match = re.match('赛前(.*?)小时(.*?)分',s2[i][1])
            s2[i][1] = int(match.group(1))*60 + int(match.group(2))#转化成据比赛开始前的剩余分钟数
        for i in range(0,len(s2)):#每一次变盘就插入一个记录
            item = CatclawTextItem()
            item['league'] = league
            item['cid'] = cid
            item['zhudui'] = zhudui
            item['kedui'] = kedui
            item['companyname'] = companyname
            item['timestamp'] = s2[i][0]
            item['resttime'] = s2[i][1]
            item['peilv'] = [s2[i][2],s2[i][3],s2[i][4]]
            item['gailv'] = [s2[i][5],s2[i][6],s2[i][7]]
            item['kailizhishu'] = [s2[i][8],s2[i][9],s2[i][10]]
            item['fanhuanlv'] = s2[i][11]
            yield item
