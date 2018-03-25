#用来在shell里测试用的代码
#决定放弃使用splash，而是直接在相应网页的ajax请求中直接得到公司列表————25.03.2018
import scrapy
from scrapy.http import FormRequest, Request
import YDM
import random
import urllib
import re
import csv
from datetime import datetime, timedelta, timezone#用来把时间字符串转换成时间
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

url = 'http://www.okooo.com/jingcai/'
request = Request(url=url,headers=header,meta=meta1)
fetch(request)
request = Request(url='http://www.okooo.com/I/?method=ok.user.settings.authcodepic',headers=header,meta=meta1)
fetch(request)
filepath = '/home/jsy/screenshot/yanzhengma.png'
with open(filepath,"wb") as f:
    f.write(response.body)#保存验证码到本地\

print('已获得验证码')
datas = randomdatas(filepath)
print('云打码已尝试一次')
request = FormRequest(url='http://www.okooo.com/I/?method=user.user.userlogin',formdata=datas,meta=meta2)
fetch(request)
request = Request(url='http://www.okooo.com/soccer/',headers=header,meta=meta2)
fetch(request)
request = Request(url='http://www.okooo.com/soccer/match/',headers=header2,meta=meta2)
fetch(request)
date = next(datelist)
request = Request(url='http://www.okooo.com/soccer/match/?date=' + date,headers=header2,meta=meta1)
fetch(request)
content1 = response.body.decode('GB18030')
sucker1 = '/soccer/match/.*?/odds/'
bisaiurl = re.findall(sucker1,content1)#获得当天的比赛列表
print(str(bisaiurl))
request = Request(url='http://www.okooo.com' + bisaiurl[97],headers=header2,meta=meta1)
fetch(request)
