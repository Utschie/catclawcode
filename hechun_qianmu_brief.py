#迁木网json文件去重
import json
import ast

data = list()
for line in open('D:\\Dropbox\\catclawcode\\hechun_qianmu.json','r'):#把数据按行读取至liebiao
    data.append(json.loads(line))

for i in range(0,len(data)):#把列表元素字典转成字符串
    data[i] = str(data[i])

data = list(set(data))#去重

for i in range(0,len(data)):#再把字符串转化成字典
    data[i] = ast.literal_eval(data[i])
    
with open('D:\\Dropbox\\catclawcode\\hechun_qianmu_brief.json','a') as f:
    for i in range(0,len(data)):
        json_str = json.dumps(data[i])
        f.write(json_str)
        f.write('\n')


