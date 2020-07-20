#何纯学长迁木网案例爬虫
#需要后期去一下重
#即便速度很低也会被封，所以要换ip以及ua
from gevent import monkey;monkey.patch_all()
import gevent
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib
import time
import random
print('正在获取国家列表')
a = requests.get('http://www.qianmu.org/offer/1-88-9-0-0-0-0-0.htm')#进入美国-金融-会计页面
soup = BeautifulSoup(a.content,'html5lib')
contrycode = soup.find_all('ul',style = 'margin-left:0px;')
sucker1 = '<a href="(/offer/.*?)">(.*?)</a>'
contrylistori = re.findall(sucker1,str(contrycode))
contrylist = list()
for i in range(0,len(contrylistori)):
    contrylist.append(['http://www.qianmu.org'+contrylistori[i][0],contrylistori[i][1]])#得到国家和网址的对应列表,6个
print('已获得国家列表')
print('正在获取大类列表')
majorlist= list()
for i in range(0,len(contrylist)):
    b = requests.get(contrylist[i][0])#进入每个国家的网页
    soup = BeautifulSoup(b.content,'html5lib')
    majorcode = soup.find_all('ul',style = "margin-bottom:10px;")
    sucker2 = '<a href="(/offer/.*?)">(.*?)</a>'
    majorlistori = re.findall(sucker2,str(majorcode))
    for j in range(0,len(majorlistori)):
        majorlist.append(['http://www.qianmu.org'+majorlistori[j][0],contrylist[i][1],majorlistori[j][1]])#获得了大类，网址，国家的列表，36个
print('已获得大类列表')
print('正在获取专业列表')
subjectlist = list()
for i in range(0,len(majorlist)):
    c = requests.get(majorlist[i][0])#进入每个大类的网页
    soup = BeautifulSoup(c.content,'html5lib')
    subjectcode = soup.find_all('ul',style = "padding-left:120px;")
    sucker3 = '<a href="(/offer/.*?)">(.*?)</a>'
    subjectlistori = re.findall(sucker3,str(subjectcode))
    for j in range(0,len(subjectlistori)):
        subjectlist.append(['http://www.qianmu.org'+subjectlistori[j][0],majorlist[i][1],majorlist[i][2],subjectlistori[j][1]])#获得小类，大类，网址，国家的对应列表，456个
print('已获得专业列表，进入网页爬取\n\n\n\n\n\n\n')

def checkip(ip):
    global header
    global UAlist
    header4 = header
    iplist = ip
    for i in range(0,len(iplist)):
        error4 = True
        mal3 = 1
        while (error4 ==True and mal3 <= 3):#总共拨三次，首拨1次重拨2次
            try:
                header4['User-Agent'] = random.choice(UAlist)#每尝试一次换一次UA
                check = requests.get('http://www.qianmu.org/offer/1-88-10-0-0-0-0-0.htm',headers = header4,proxies = {"http":"http://"+ iplist[i]},timeout = 6.5)
            except Exception as e:
                error4 = True
                mal3 = mal3 + 1
                if mal3 > 3:
                    iplist[i] = ''
                    print('第' + str(i) + '个IP不合格，已去除')
            else:
                error4 = False
                print('第' + str(i) + '个IP合格')
    while '' in iplist:
        iplist.remove('')
    return iplist





#接下来是进入每一个单个专业，每一个单个专业下面有许多页面，每一个页面上的案例同时抓取
def datatofile(url,contry,major,subject):
    global UAlist
    global proxylist
    global header
    header1 = header
    header1['User-Agent'] = random.choice(UAlist)
    info = {}
    error2 = True
    mal0 = 1
    while (error2 == True and mal0 <= len(proxylist)):
        if mal0 == len(proxylist):
            print('IP已失效，正在重新获取ip')
            error4=True
            while(error4==True):
                try:
                    proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=4f85e66b7f9f4297b146af4df281cd13&returnType=1&count=1') #接入混拨代理
                    print('已获取IP')
                    proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                    print('正在检查IP')
                    proxylist = checkip(proxylist)
                    for j in range(0,len(proxylist)):
                        proxylist[j] = {"http":"http://" + proxylist[j],}
                    print(proxylist)
                    mal0 = 1
                    error4 =False
                except Exception as e:
                    time.sleep(15)
                    error4 = True
        try:
            a = requests.get(url,proxies = random.choice(proxylist),headers = header1,timeout = 6.5)#进入网页
            soup = BeautifulSoup(a.content,"html5lib")
            tds = soup.find_all('td')
            idsucker ='id=(.*)' 
            info['ID'] = re.search(idsucker,url).group(1)
            info['国家']=contry
            info['大类'] = major
            info['专业'] = subject
            info['本科学校'] = tds[1].text.strip()
            info['本科专业'] = tds[3].text.strip()
            info['本科GPA'] =tds[5].text.strip()
            info['本科排名'] = tds[7].text.strip()
            info['研究生学校'] = tds[9].text.strip()
            info['研究生专业'] = tds[11].text.strip()
            info['研究生GPA'] = tds[13].text.strip()
            info['研究生排名'] = tds[15].text.strip()
            info['TOEFL/IELTS'] = tds[17].text.strip()
            info['TOEFL/IELTS口语'] = tds[19].text.strip()
            info['GRE/GMAT/LSAT'] = tds[21].text.strip()
            info['GRE写作'] = tds[23].text.strip()
            info['GRE Sub'] = tds[25].text.strip()
            info['推荐人力度'] = tds[27].text.strip()
            sucker1 = '科研-(.*?)\r'
            info['科研'] = re.search(sucker1,a.text).group(1)
            sucker2 = '科研经历：(.*?)\r'
            try:
                info['科研经历'] = re.search(sucker2,a.text).group(1)
            except Exception as e:
                info['科研经历'] = ''
            sucker3 = '工作与实习经历：(.*?)\r'
            try:
                info['工作与实习经历'] = re.search(sucker3,a.text).group(1)
            except Exception as e:
                info['工作与实习经历'] = ''
            sucker4 = '交流经历：(.*?)\r'
            try:
                info['交流经历'] = re.search(sucker4,a.text).group(1)
            except Exception as e:
                info['交流经历'] = ''
            sucker5 = '所获奖项：(.*?)\r'
            try:
                info['所获奖项'] = re.search(sucker5,a.text).group(1)
            except Exception as e:
                info['所获奖项'] = ''
            luqulist = list()
            table = soup.find_all('table')[1].find_all('tr')
            for i in range(1,len(table)):
                juqiqingkuang = table[i].findAll('th')
                uniname = juqiqingkuang[0]
                project = juqiqingkuang[1]
                degree = juqiqingkuang[2]
                result = juqiqingkuang[3]
                luqulist.append([uniname.get_text(),project.get_text(),degree.get_text(),result.get_text()])
            info['录取结果'] = luqulist
            json_str = json.dumps(info)
            with open('D:\\Dropbox\\catclawcode\\hechun_qianmu.json', 'a') as f:
                f.write(json_str)
                f.write('\n')
            print(url+'获取完毕')
            error2 = False
        except Exception as e:
            mal0 = mal0 + 1
            print(url+'出错，正在重试')
            error2 = True
        




def coprocess(urllist,contry,major,subject):
    ge = list()
    for i in urllist:
        ge.append(gevent.spawn(datatofile,i,contry,major,subject))
    gevent.joinall(ge)


def dangezhuanye(subject):#subject是subjectlist里的元素
    global UAlist
    global proxylist
    global header
    header1 = header
    header1['User-Agent'] = random.choice(UAlist)
    error2 = True
    mal0 = 1
    while (error2 == True and mal0 <= len(proxylist)):
        if mal0 == len(proxylist):
            print('IP已失效，正在重新获取ip')
            error4=True
            while(error4==True):
                try:
                    proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=4f85e66b7f9f4297b146af4df281cd13&returnType=1&count=1') #接入混拨代理
                    print('已获取IP')
                    proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                    print('正在检查IP')
                    proxylist = checkip(proxylist)
                    for j in range(0,len(proxylist)):
                        proxylist[j] = {"http":"http://" + proxylist[j],}
                    print(proxylist)
                    mal0 = 1
                    error4 =False
                except Exception as e:
                    time.sleep(15)
                    error4 = True
        try:
            a = requests.get(subject[0],proxies = random.choice(proxylist),headers = header1,timeout = 6.5)
            sucker = '\.\.\.</a></li><li><a href=\'\?p=(.*?)\'>'
            try:
                pagezahl = int(re.search(sucker,a.text).group(1))
            except Exception as e:
                pagezahl = 1
            error2 = False
        except Exception as e:
            print('单个专业1出错')
            mal0 = mal0 + 1
            error2 = True
    print('进入专业'+subject[1]+'_'+subject[2]+'_'+subject[3]+'，共'+str(pagezahl)+'页')
    for j in range(1,pagezahl+1):   
        error3 = True
        mal = 1
        while (error3 == True and mal <= len(proxylist)):
            if mal == len(proxylist):
                print('IP已失效，正在重新获取ip')
                error5=True
                while(error5==True):
                    try:
                        proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=4f85e66b7f9f4297b146af4df281cd13&returnType=1&count=1') #接入混拨代理
                        print('已获取IP')
                        proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                        print('正在检查IP')
                        proxylist = checkip(proxylist)
                        for j in range(0,len(proxylist)):
                            proxylist[j] = {"http":"http://" + proxylist[j],}
                        print(proxylist)
                        mal0 = 1
                        error5 =False
                    except Exception as e:
                        time.sleep(15)
                        error5 = True
            try:
                a = requests.get(subject[0]+'?p='+str(j),proxies = random.choice(proxylist),headers = header1,timeout = 6.5)#进入网页
                sucker4 = '(/casesinfo\?id=.*?)"'
                caselist = re.findall(sucker4,a.text)#得到当页的case网址列表
                if caselist == []:
                    continue
                caselist = list(set(caselist))#列表去重
                for i in range(0,len(caselist)):
                    caselist[i] = 'http://www.qianmu.org'+caselist[i]#完成列表
                coprocess(caselist,subject[1],subject[2],subject[3])#列表中的数据同时抓取
                print(subject[1]+'_'+subject[2]+'_'+subject[3]+'第'+str(j)+'页获取完毕')
                error3 = False
            except Exception as e:
                mal = mal + 1
                error3 = True         
    print('\n\n\n\n'+subject[1]+'_'+subject[2]+'_'+subject[3]+'获取完毕')


def main():
    global proxylist
    for i in range(0,len(subjectlist)):
        time.sleep(15)
        error6 = True
        while(error6==True):
            try:
                proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/applyStaticProxy?spiderId=4f85e66b7f9f4297b146af4df281cd13&returnType=1&count=1') #接入混拨代理
                print('已获取IP')
                proxylist = re.findall('(.*?)\\r\\n',proxycontent.text)
                print('正在检查IP')
                proxylist = checkip(proxylist)
                for j in range(0,len(proxylist)):
                    proxylist[j] = {"http":"http://" + proxylist[j],}
                print(proxylist)
                mal0 = 1
                error6 =False
            except Exception as e:
                time.sleep(15)
                error6 = True
        dangezhuanye(subjectlist[i])
    
start = time.time()
UAcontent = urllib.request.urlopen('file:///D:/data/useragentswitcher.xml').read()
UAcontent = str(UAcontent)
UAname = re.findall('(useragent=")(.*?)(")',UAcontent)
UAlist = list()
for z in range(0,int(len(UAname))):
    UAlist.append(UAname[z][1])

UAlist = UAlist[0:586]#这样就得到了一个拥有586个UA的UA池
UAlist.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')#再加一个
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
main()
print('任务完成')
    

    



