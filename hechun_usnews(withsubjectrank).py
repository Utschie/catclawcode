#何纯学长关于USnews大学排名的代码
from gevent import monkey;monkey.patch_all()
import gevent
import requests
from bs4 import BeautifulSoup
import re
import json



def autologin():
    global r
    global header
    url = 'https://secure.usnews.com/member/login?ref=https%3A%2F%2Fwww.usnews.com%2Fbest-colleges'
    datas = 'username=rogerhoooo%40yahoo.com&password=bibi1218&referer='
    print('正在登陆')
    prelogin = r.get('https://www.usnews.com/best-colleges',headers = header)#y预登陆时只需要有一个headers就好
    login = r.post(url,headers = header,data = datas)



def tiquziduan(uni):
    global r
    global header
    uniattribute={}
    sucker0 = ' <span class="text-strong">(.*?) in National Universities'
    uniattribute['Rank'] = re.search(sucker0,uni).group(1)
    sucker1 = '<a href="(.*?)">(.*?)</a>'
    uniattribute['url'] = 'https://premium.usnews.com' + re.search(sucker1,uni).group(1)
    uniattribute['name'] = re.search(sucker1,uni).group(2)
    uniattribute['overallurl'] = uniattribute['url'] +'/overall-rankings'
    sucker2 = '<div>\n.*?\n\n'
    a = re.findall(sucker2,uni)
    sucker3 = r'(\$.*?)\n'
    try:
        uniattribute['Tuition and Fees'] = re.search(sucker3,a[0]).group(1)
    except Exception as e:
        uniattribute['Tuition and Fees'] = 'N/A'
    sucker4 = '<div>\n(.*?)\n\n'
    uniattribute['Enrollment'] = re.search(sucker4,a[1]).group(1).strip()
    sucker5 = '<div>\n(.*?)<span'
    uniattribute['SAT'] = re.search(sucker5,a[2]).group(1).strip()
    uniattribute['ACT'] = re.search(sucker5,a[3]).group(1).strip()
    page = r.get(uniattribute['url'],headers = header)
    sucker6 = 'data-test-id="">\n(.*?)<sup class="text-alert">'
    try:
        uniattribute['Median starting salary of alumni'] = re.search(sucker6,page.text).group(1).strip()
    except Exception as e:
        uniattribute['Median starting salary of alumni'] = 'N/A'
    sucker7 = 'data-test-id="c_select_class">\n(.*?)</span>'
    uniattribute['Selectivity'] = re.search(sucker7,page.text).group(1).strip()
    sucker8 = 'data-test-id="r_c_accept_rate">\n(.*?)</span>'
    uniattribute['Acceptance rate'] = re.search(sucker8,page.text).group(1).strip()
    sucker9 = 'data-test-id="application_deadline">\n(.*?)</span>'
    uniattribute['Application deadline'] = re.search(sucker9,page.text).group(1).strip()
    sucker10 = '<span class="bar-percentage-chart__stat">(.*?)</span>'
    uniattribute['Class sizes(<20,20-49,>=50)'] = re.findall(sucker10,page.text)
    sucker11 = 'data-test-id="v_student_faculty_ratio">\n(.*?)</span>'
    uniattribute['Student-faculty ratio'] = re.search(sucker11,page.text).group(1).strip()
    sucker12 = 'data-test-id="grad_rate_4_year">\n(.*?)</span>'
    uniattribute['4-year graduation rate'] = re.search(sucker12,page.text).group(1).strip()
    sucker13 = '\n(.*?)full time,(.*?)part time</span>'
    c = re.search(sucker13,page.text)
    try:
        uniattribute['Total faculty(fulltime,parttime)'] = [c.group(1).strip(),c.group(2).strip()]
    except Exception as e:
        uniattribute['Total faculty(fulltime,parttime)'] = 'N/A'
    overallpage = r.get(uniattribute['overallurl'],headers = header)
    sucker14 = '<a href="(.*?)">Grad School Rankings'
    try:
        subjecturl = re.search(sucker14,overallpage.text).group(1)
        subjectpage = r.get(subjecturl,headers=header)#得到有具体专业排名的网页
        soup = BeautifulSoup(subjectpage.content,'html5lib')
        subjectlistcode = soup.find_all('li','has-badge RankList__ListItem-y61oaj-1 cvtOtc')#得到了包含所有大专业的代码列表，大专业下面还有小专业
        sucker15 = '#<!-- -->(.*?)<'
        sucker16 = 'name="(.*?)"'
        for i in range(0,len(subjectlistcode)):
            ranklist = re.findall(sucker15,str(subjectlistcode[i]))#得到一堆排名数字的列表
            namelist = re.findall(sucker16,str(subjectlistcode[i]))#得到排名数字对应的名称的列表
            if len(namelist) > 1:
                for j in range(1,len(namelist)):#如果下面有小专业则把专业大类标出来
                    namelist[j] = namelist[0]+'__'+namelist[j]
            elif len(namelist) == 0:
                continue
            try:
                for s in range(0,len(ranklist)):
                    uniattribute[namelist[s]] = ranklist[s] 
            except Exception as e:
                pass
    except Exception as e:
        pass
    json_str = json.dumps(uniattribute)
    with open('D:\\Dropbox\\catclawcode\\hechun_usnews.json', 'a') as f:
        f.write(json_str)
        f.write('\n')



def coprocess(unilist):#用协程的方式并发打开网页
    ge = list()
    for i in unilist:
        ge.append(gevent.spawn(tiquziduan,i))
    gevent.joinall(ge)

def main():
    global r
    global header
    autologin()
    for pagenum in range(1,16):
        url = 'https://premium.usnews.com/best-colleges/rankings/national-universities?_mode=table&_page=' + str(pagenum)
        table = r.get(url,headers = header)
        soup = BeautifulSoup(table.content,'html5lib')
        tr = soup.find_all('tr')
        droplist = list() 
        for i in [0,1,2,3]:
            droplist.append(tr[6*i])
        for i in droplist:
            tr.remove(i)
#于是得到了装有该页20个学校的标签
        unilist = list(tr)#列表化
        for i in range(0,len(unilist)):#字符串化
            unilist[i] = str(unilist[i])
        coprocess(unilist)#对于一页下的20个学校用协程抓取
        print('第'+ str(pagenum)+'页爬取成功')
    url = 'https://premium.usnews.com/best-colleges/rankings/national-universities?_mode=table&_page=16'
    table = r.get(url,headers = header)
    soup = BeautifulSoup(table.content,'html5lib')
    tr = soup.find_all('tr')
    droplist = list() 
    for i in [0,1,2]:
        droplist.append(tr[6*i])
    for i in droplist:
        tr.remove(i)
    #于是得到了装有该页20个学校的标签
    unilist = list(tr)#列表化
    for i in range(0,len(unilist)):#字符串化
        unilist[i] = str(unilist[i])
    coprocess(unilist)#对于一页下的20个学校用协程抓取
    print('第16页爬取成功')

        

r = requests.Session()
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
main()






                    


        


