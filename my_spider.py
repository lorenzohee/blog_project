# encoding:utf-8

import re
import urllib.request
import urllib
from urllib import error
import queue
import threading
import os
from bs4 import BeautifulSoup
import sqlite3
import time


class MyRobot(threading.Thread):
	def __init__(self, num):
		threading.Thread.__init__(self)
		self.num = num

	def save_data(self, data, filename):
		if not os.path.exists('blog'):
			blog_path = os.path.join(os.path.abspath('.'),'blog')
			os.mkdir(blog_path)
		try:
			fout = open('./blog/' + filename + '.html', 'wb')
			fout.write(data)
		except IOError as e:
			print('IO error:', e)

	def find_title(self,data):
		data = data.decode('gb2312')
		begin = data.find(r'<title') + 7
		end = data.find('\r\n',begin)
		title = data[begin:end]
		return title

	def db_save(self, data):
		conn = sqlite3.connect('data.sqlite')
		c = conn.cursor()
		sql = "INSERT INTO articles (title, content, article_id, url_from, is_published, articleType_id, create_time, update_time, source_id, num_of_view) VALUES ('%s','%s', %s, '%s', 0, 1, '%s', '%s', 1, 1)"%(data['title'], data['content'], data['article_id'], data['url'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

		c.execute(sql)
		conn.commit()

	def run(self):
		url = 'http://www.weipet.cn/common/huli/huli-a' + str(self.num) + '.html'
		try:
			res = urllib.request.urlopen(url)
			data = res.read()
			html=BeautifulSoup(data,'html.parser')
			#print(html.find_all('table')[9])
			# self.save_data(data,html.title.get_text())
			postData = {
				'title': html.title.get_text(),
				'content': html.find_all('table')[9],
				'article_id': self.num,
				'url': url
			}
			self.db_save(postData)
		except error.HTTPError as e:
			print(e.reason)

if __name__ == '__main__':
	# conn = sqlite3.connect('data.sqlite')
	# c = conn.cursor()
	# max_id = c.execute('select max(article_id) from articles')
	# next_id = 0
	# for xx in max_id:
	# 	next_id = xx[0]
	# next_id = next_id+1
	# print(next_id)
	# conn.close();
	# while true
	# 	conn = sqlite3.connect('data.sqlite')
	# 	c = conn.cursor()
	# 	max_id = c.execute('select id from articles where id=%s'%(next_id))
	# 	if max_id.length>0:
	# 		thread = MyRobot(next_id)
	# 		thread.start()
	# 	else:
	# 		break
	# 	next_id = next_id+1
	# 	print(next_id)
	# 	conn.close();

	for i in range(28):
		thread = MyRobot(i)
		thread.start()
