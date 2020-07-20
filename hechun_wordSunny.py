#何纯学长关于https://www.wordsunny.com/tutorList.html的任务
from gevent import monkey;monkey.patch_all()
import gevent
import requests
from bs4 import BeautifulSoup
import re
import csv
ziduan = {}
ziduan['url'] = ''
ziduan['评分'] ='' 
ziduan['姓名'] = ''
ziduan['订购人数'] ='' 
ziduan['学位'] =''
ziduan['服务内容'] ='' 
ziduan['擅长领域'] = ''
ziduan['教育信息'] = ''
with open('D:\\Dropbox\\catclawcode\\hechun.csv','w',encoding = 'gb18030') as f:
    w = csv.writer(f)
    w.writerow(ziduan.keys())

def tiquziduan(geren):
    ziduan = {}
    ziduan['url'] = 'https://www.wordsunny.com/' + re.search('ahref="(tutorListDetail-.*?html)"',geren).group(1)
    ziduan['pingfen'] = re.search('<p>评分：<span>(.*?)</span></p>',geren).group(1)
    ziduan['name'] = re.search('<h2>(.*?)</h2>',geren).group(1)
    ziduan['dinggourenshu'] = re.search('<i>(.*?)</i>人订购',geren).group(1)
    ziduan['xuewei'] = re.search('人订购</span><p>(.*?)</p></div><divclass="biaoqians">',geren).group(1).replace('&nbsp;&nbsp','')
    try:
        ziduan['fuwuneirong'] = re.search('服务内容：(.*)&nbsp;&nbsp;',geren).group(1).replace('&nbsp;&nbsp','')
    except Exception as e:
        ziduan['fuwuneirong'] = '' 
    ziduan['shanchanglingyu'] = re.search('擅长领域：(.*?)</p>',geren).group(1).replace('，',';')
    gerenzhuye = requests.get(ziduan['url'])
    soup = BeautifulSoup(gerenzhuye.content,"html5lib")
    jiaoyuinfosoup = soup.find_all(class_ = 'jiaoyuinfo')
    jiaoyuinfolist = list(jiaoyuinfosoup)#列表化
    for i in range(0,len(jiaoyuinfolist)):#字符串化
        jiaoyuinfolist[i] = str(jiaoyuinfolist[i])
    for i in range(0,len(jiaoyuinfolist)):
        jiaoyuinfolist[i] = re.search('<h3>(.*?)</h3>',jiaoyuinfolist[i]).group(1).replace('&amp;','&')+'_'+ re.findall('<p>(.*?)</p>',jiaoyuinfolist[i])[0] +'_'+ re.findall('<p>(.*?)</p>',jiaoyuinfolist[i])[1]
    jiaoyuinfo = str()
    for i in jiaoyuinfolist:
        jiaoyuinfo  = jiaoyuinfo + ';'+i
    jiaoyuinfo.replace('&amp;','&')
    ziduan['jiaoyuinfo'] = jiaoyuinfo
    #shejilingyusoup = soup.find_all(class_ = 'renshu')
    #shejilingyulist = list(shejilingyusoup)
    #for i in range(0,len(shejilingyulist)):
    #    shejilingyulist[i] = str(shejilingyulist[i])
    #for i in range(0,len(shejilingyulist)):
    #    shejilingyulist[i] = re.findall('<span>(\D*?)人</span>',shejilingyulist[i])[0] + '_' + re.findall('<span>(\d*?)</span>',shejilingyulist[i])[0]
    #shejilingyu = str()
    #for i in shejilingyulist:
    #    shejilingyu = i  + ';' + shejilingyu
    #ziduan['shejilingyu'] = shejilingyu
    with open('D:\\Dropbox\\catclawcode\\hechun.csv','a',encoding = 'gb18030') as f:
        w = csv.writer(f)
        w.writerow(ziduan.values())






def coprocess(li):#用协程的方式并发打开网页
    ge = list()
    for i in li:
        ge.append(gevent.spawn(tiquziduan,i))
    gevent.joinall(ge)

    
    

def main():
    for i in range(1,65):
        url = 'https://www.wordsunny.com/tutorList.html?type=all&search=&sever=all&linkname=all&education=all&''page='+str(i)+'#search'
        a = requests.get(url)
        sucker0 = '<li>\r\n\t\t\t\t\t\t\t<a href="tutorListDetail.*?target="_blank"[\s\S]*?</a>'
        li = re.findall(sucker0,a.text)#取回每页8个人的信息
        for b in range(0,len(li)):#去掉空格和换行符
            li[b] = li[b].replace('\t','')
            li[b] = li[b].replace('\r\n','')
            li[b] = li[b].replace(' ','')
        #for c in range(0,len(li)):
        #    tiquziduan(li[c])
        #    print('第'+str(c)+'个人爬取成功')
        coprocess(li)
        print('第'+ str(i) + '页爬取成功')

main()









