#!/usr/bin/env python
#_*_coding:utf-8_*_


#用selenium获取cookie
from selenium import webdriver
from PIL import Image
import YDM
driver = webdriver.Chrome()#打开一个chrome浏览器
driver.get('https://www.weibo.com/')
element = driver.find_element_by_name('username')#输入用户名
element.send_keys("18212831689")
element = driver.find_element_by_name('password')#输入密码
element.send_keys("921202jsy")
element = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/div[3]/div[3]/a/img')
left = element.location['x']
top = element.location['y']
elementWidth = element.location['x'] + element.size['width']
elementHeight = element.location['y'] + element.size['height']
filepath = '/home/jsy/screenshot/yanzhengma.png'
yanzhengma = Image.open(filepath)
yanzhengma = yanzhengma.crop((left, top, elementWidth, elementHeight))
yanzhengma.save(filepath)#获得验证码
