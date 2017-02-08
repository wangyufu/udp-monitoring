#!/usr/bin/env python
# coding:utf8
from socket import *
import os, threading, time, datetime, shutil

HOST = ''
PORT = 21567
BUFSIZ = 2048
ADDR = (HOST, PORT)
udpSerSock = socket(AF_INET, SOCK_DGRAM)
udpSerSock.bind(ADDR)
dic = {}
ip_set = set()
file_path = '/zhangyu/server_monitoring/'

def load():
    string = ''
    for k in dic.keys():
        today = time.strftime('%m%d', time.localtime(time.time()))+'/'+time.strftime('%m%d', time.localtime(time.time()))+'_'+k.split('.')[3]+'.html'
        Article_60 = 'ipieuvre_monitor_message_article60_' + k.split('.')[3] + '.html'
        if not os.path.exists(file_path+'log/'+today):
            os.system('touch ' + file_path+'log/'+today)
            os.system('mkdir -p ' + file_path+'log/'+time.strftime('%m%d', time.localtime(time.time())))
        if not os.path.exists(file_path+Article_60):
            os.system('touch ' + file_path+Article_60 )
        s = k
        for l in dic[k]:
            s += ' '+l
        string += ','.join(s.split()) + '\n#'
        string1 = str(int(time.time()))+':'+','.join(s.split()) + '\n#'
        if len(open(file_path+Article_60, 'rU').readlines()) > 59 :
            os.system('sed -i "1d" '+file_path+Article_60)
        with open(file_path+Article_60, 'a') as f:
            f.write(string1)	
        with open(file_path+'log/'+today, 'a') as f:
            f.write(string1)
        dic.pop(k)
    with open(file_path + 'ipieuvre_monitor_message.html', 'wt') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n#' + string)
    timer = threading.Timer(10.0, load)
    timer.start()

	
def remove():
    for k in list(ip_set):
        overdue = str(datetime.date.today()+datetime.timedelta(-30))[5:7] + \
                str(datetime.date.today() + datetime.timedelta(-30))[8:]
        if os.path.exists(file_path+'log/'+overdue):
            shutil.rmtree(file_path+'log/'+overdue)
    timer2 = threading.Timer(21600.0, remove)
    timer2.start()

# 每十秒向文件写入一次数据	
timer = threading.Timer(10.0, load)
timer.start()
# 定时删除历史文件
timer2 = threading.Timer(21600.0, remove)
timer2.start()

while True:
    data, addr = udpSerSock.recvfrom(BUFSIZ)
    dic[addr[0]] = data.split()
    ip_set.add(addr[0])


