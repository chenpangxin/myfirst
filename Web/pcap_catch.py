#coding=utf-8
from multiprocessing import Process,Queue
import os
import time
from client_db import con
import sys
import zipfile
import subprocess


reload(sys)
sys.setdefaultencoding('utf-8')

class dumpTcp():
	def __init__(self):
		#用于读写任务
		self.q = Queue()
		#用于判断当前执行任务的数量
		self.q1 = Queue()
	# 创建一个任务就创建一个进程
	def action(self):
		a = Process(target=self.read)
		a.start()

	def read(self):
		while True:
			msg2 =  self.q.get()
			if msg2 != '':
				self.info(msg2)

# 创建任务，放入数据库和队列
	def write(self,msg):
		s=msg.split(',')
		coll = con()
		data = coll.find_one()
		# 如果数据库为空，那设第一条id为0，其他添加的数据在当前最大id上加1
		if data is None:
			if s[0]=='1':
				# time = self.timeChange(int(s[1]))
				coll.insert_one({"_id": 1, "setType": s[0],"time":s[1],"size":'',"taskName":s[2],"startTime":s[3],"ip":s[4],"pid":'',"pypid":'',"download":'',"endTime":'',"packSize":'',"status":'Waiting',"finish":'N'})
			elif s[0]=='0':
				# size = self.sizeChange(float(s[1]))
				coll.insert_one({"_id": 1, "setType": s[0],"time":'',"size":s[1],"taskName":s[2],"startTime":s[3],"ip":s[4],"pid":'',"pypid":'',"download":'',"endTime":'',"packSize":'',"status":'Waiting',"finish":'N'})
		else:
			for i in coll.find().sort([("_id",-1)]).limit(1):
				last_id = i['_id']
				if s[0]=='1':
					# time = self.timeChange(int(s[1]))
					coll.insert_one({"_id":last_id+1,"setType": s[0],"time":s[1],"size":'',"taskName":s[2],"startTime":s[3],"ip":s[4],"pid":'',"pypid":'',"download":'',"endTime":'',"packSize":'',"status":'Waiting',"finish":'N'})
				elif s[0]=='0':
					# size = self.sizeChange(float(s[1]))
					coll.insert_one({"_id":last_id+1,"setType": s[0],"time":'',"size":s[1],"taskName":s[2],"startTime":s[3],"ip":s[4],"pid":'',"pypid":'',"download":'',"endTime":'',"packSize":'',"status":'Waiting',"finish":'N'})
		for i in coll.find().sort([("_id",-1)]).limit(1):
			self.q.put(msg+','+str(i['_id']))
	# 抓包逻辑
	def info(self,msg3):
		self.q1.put(str(os.getpid()))
		coll = con()
		s = msg3.split(',')
		flag, size, name, run_time, ip, id = s[0], s[1], s[2], s[3], s[4], s[5]
		coll.update({"_id": int(s[5])}, {"$set": {"pypid": str(os.getpid())}})
		# 最终文件压缩成的名字,其他文件都被删除
		zip_name = u'/home/Web_demo/test/Web/pcapzip/' + name + '.zip'
		# 设定的时间如果小于当前时间则不符合要求
		# source = int(time.mktime(time.strptime(run_time, "%Y-%m-%d %H:%M:%S")))
		source = int(time.mktime(time.strptime(run_time, "%Y-%m-%d %H:%M")))
		if source > int(time.time()):
			if flag == '1':
				sign1 = 1
				sign2 = 1
				# 在死循环中判断到了指定的时间进行抓包，同时拿到pid,通过kill pid来终止抓包
				while (sign1):
					if source == int(time.time()):
						sign1 = 0
				sub = subprocess.Popen('tcpdump -i ens33  -s 0  -Z root -w /home/Web_demo/test/Web/pcapzip/'+name+'.pcap host ' + ip,shell=True)
				PID = str(sub.pid)
				coll.update({"_id": int(s[5])}, {"$set": {"pid": PID}})
				coll.update({"_id": int(s[5])}, {"$set": {"status": 'Catching'}})
				# 到了时间就kill掉这个子进程
				while (sign2):
					if source+int(size) == int(time.time()):
						subprocess.call('kill -9 ' + PID, shell=True)
						sign2=0
				# 把结束时间加入
				over_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
				coll.update({"_id": int(s[5])}, {"$set": {"endTime": over_time}})
				oldname = u'/home/Web_demo/test/Web/pcapzip/' + name + '.pcap'
				# 判包的大小
				# filesize = self.getPcapSize(oldname)
				filesize = os.path.getsize(oldname)
				coll.update({"_id": int(s[5])}, {"$set": {"packSize": str(filesize)}})
				# 压缩
				f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
				f.write(oldname, name + '.pcap')
				f.close()
				os.remove(oldname)
				coll.update({"_id": int(s[5])}, {"$set": {"download": name + '.zip'}})
				coll.update({"_id": int(s[5])}, {"$set": {"finish": 'Y'}})
				coll.update({"_id": int(s[5])}, {"$set": {"status": 'Finish'}})
			elif flag == '0':
				sign3 = 1
				sign4 = 1
				while (sign3):
					if source == int(time.time()):
						sign3 = 0
				sub2 = subprocess.Popen('tcpdump -i ens33  -s 0  -C ' + size + ' -Z root -w /home/Web_demo/test/Web/pcapzip/' + name + '.pcap host ' + ip,shell=True)
				PID = str(sub2.pid)
				coll.update({"_id": int(s[5])}, {"$set": {"pid": PID}})
				coll.update({"_id": int(s[5])}, {"$set": {"status": 'Catching'}})
				oldname = u'/home/Web_demo/test/Web/pcapzip/' + name + '.pcap'
				rm_name = u'/home/Web_demo/test/Web/pcapzip/' + name + '.pcap1'
				# 抓到所需大小的包会生成.pcap1/.pcap2...的文件，根据生成的.pcap1来判断是否完成，完成之后，将判断条件的.pcap1删除，将所需文件压缩，将原文件删除
				while (sign4):
					if os.path.exists(rm_name) == True:
						subprocess.Popen('kill -9 ' + PID, shell=True)
						os.remove(rm_name)
						sign4 = 0
				over_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(time.time()))
				coll.update({"_id": int(s[5])}, {"$set": {"endTime": over_time}})
				# filesize = self.getPcapSize(oldname)
				filesize = os.path.getsize(oldname)
				coll.update({"_id": int(s[5])}, {"$set": {"packSize": filesize}})
				f = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
				f.write(oldname, name + '.pcap')
				f.close()
				os.remove(oldname)
				coll.update({"_id": int(s[5])}, {"$set": {"download": name + '.zip'}})
				coll.update({"_id": int(s[5])}, {"$set": {"finish": 'Y'}})
				coll.update({"_id": int(s[5])}, {"$set": {"status": 'Finish'}})
		else:
			coll.update({"_id": int(s[5])}, {"$set": {"status": 'TimeError'}})
		self.q1.get()

	# 字节bytes转化kb\m\g
	def formatSize(self,bytes):
		try:
			bytes = float(bytes)
			kb = bytes / 1024
		except:
			# print("传入的字节格式不对")
			return "Error"
		if kb >= 1024:
			M = kb / 1024
			if M >= 1024:
				G = M / 1024
				return "%.2fG" % (G)
			else:
				return "%.2fM" % (M)
		else:
			return "%.2fkb" % (kb)
	# 获取文件大小
	def getPcapSize(self,path):
		try:
			size = os.path.getsize(path)
			return self.formatSize(size)
		except Exception as err:
			print(err)
#将所抓包大小，时间，转换单位
	def sizeChange(self,M):
		M = float(M)
		if M >= 1024:
			G = M / 1024
			return "%.2fG" % (G)
		else:
			return "%.fM" % (M)
	def timeChange(self,T):
		t = int(T)
		if t >= 60:
			M = t/60
			s = t%60
			return "%d分%d秒" % (M,s)
		elif t<60:
			return "%d秒" % t
pcap = dumpTcp()
