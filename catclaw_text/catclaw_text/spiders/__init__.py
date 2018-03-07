# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


#scrapy爬虫默认情况下是每一个爬虫或者说每一个project是与对面服务器连接的一个session。所以实际上一个project运行完一圈儿（比如catclaw_text就是一个project）就相当于
#okooospiderman3.0_advanced中的一个用户爬取一天数据的过程，因为一个用户登录用的就是一个session。即便在爬取的一天各场比赛和各个公司用了协程并发的方式，
#它依然是在一个session内。
#所以一个爬虫project与一个okooospiderman3.0_advanced是一样的
#而所谓分布式爬虫指的实际上就是同时开启多个session，在diy爬虫中对应的就是改一下日期，
#然后开好几个终端的样子。只不过在scrapy里可以利用包来一个命令开启多个终端进行爬取。


#所以本爬虫的结构为：spiders发出初始登录请求①，得到response⑤返回给spiders⑥，发现登录成功后继续发出请求⑦，进入当天比赛得到response⑤并返回⑥给spiders，spiders得到
#了当天的比赛列表后再度发出请求⑦，进入单场比赛，途中经由splash加载出动态呈现的公司列表，从response⑤返回给spiders⑥，spiders得到单场比赛的公司列表后第三次发出请求⑦（同
#时也是第四次发出请求），从response⑤返回给spiders⑥，得到item⑦经由spidermiddlewares传给ITEM_PIPELINES⑧，入库，同时通知spiders开启下一个session⑦登录请求，即第二天的爬取。
#与此同时，分布式的其他终端也在进行同样的动作，只是范围不同。（其中序号①⑤⑥⑦代表的是scrapy教程中architecture overview中
#的序号）————2018年3月7日

#本程序的开发过程是，先使project做成从开始到结束只运行一个session，即只爬取一天比赛就结束的程序。然后再看能否在一个project中循环地开启新session。————2018年3月8日
