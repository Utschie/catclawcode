#二哥郑交所数据爬虫
import requests
header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
header['Referer'] = 'http://123.15.58.23/CIDwebApp/Login.aspx'
header['Upgrade-Insecure-Requests'] = '1'
datas = '__VIEWSTATE=%2FwEPDwUKMTQzNjIzNjY3N2QYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgIFDEltYWdlQnV0dG9uMQUIQ2hlY2tCb3j7aJSeFJfixGz2DWQaQw5pl28%2FxA%3D%3D&__EVENTVALIDATION=%2FwEWBQLOpuTIBAKFstioBwLSwpnTCAL6v9n7BgLE1563CiZFj8sVkjUMo1GV%2FzRs8YbXXMYT&Text_LoginUser=czce1&ImageButton1.x=32&ImageButton1.y=24&Text_LoginPass=CZCE111'
header['Cookie'] = 'ASP.NET_SessionId=wtuxfzmdzcbyfl45ycxmu155; cidwebapp=loginuser='
header['Origin'] = 'http://123.15.58.23'
header['Host'] = '123.15.58.23'
header['Connection'] = 'keep-alive'
r = requests.Session()
r.post('http://123.15.58.23/CIDwebApp/Login.asp',headers=header,data=datas)