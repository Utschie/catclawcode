#罕妹妹的流量爬虫
import requests
import urllib
import random
import time
import re
UAlist = list()
UAlist.append('Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.5.2.501 NetType/WIFI')
UAlist.append('Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI')

def IPapi():
    error = True
    while(error == True):
        proxycontent = requests.get('http://api.xdaili.cn/xdaili-api//privateProxy/getDynamicIP/DD2018433841Oyce0H/c71627197db611e7bcaf7cd30abda612?returnType=1')#接入独享代理
        if str(re.search('{"ERRORCODE".*',proxycontent.text)) != 'None':
            print('提取ip出错')
            time.sleep(60)
            error = True
        else:
            proxy = {"http":"http://"+ proxycontent.text,}
            return proxy
            error = False


url = 'http://mp.weixin.qq.com/s/o0XvkhGG96-456H7USDheg'
for i in range(0,10000):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}#设置UA假装是浏览器
    header['User-Agent'] = random.choice(UAlist)
    r = requests.Session()#开启会话
    r.proxies = IPapi()
    r.get(url)
    print('正在进行第'+str(i)+'次浏览')
    time.sleep(random.uniform(15,60))

print('完成')
