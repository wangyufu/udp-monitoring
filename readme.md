udp-monitoring
==

**运行环境：python2.7、linux系统**   

**创建文件目录、修改hosts、调试clinet端的命令**  

**启动命令:nohup python jk_server.py &** 

---

server端会每10s在文件目录创建当前监控、最近60条、历史的csv文件    
client端会每5s向server端发送数据    
server端一定时间会删除30天前的历史文件
