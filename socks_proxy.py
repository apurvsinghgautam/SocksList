
import os
import re
import json
import requests
import maxminddb
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta

class ProxyList():
	
	def __init__(self):
		os.environ['PATH']=os.environ['PATH'] + ':/opt/phantomjs-2.1.1-linux-x86_64/bin'
		self.url = 'https://sockslist.net/proxy/server-socks-hide-ip-address/'
		self.driver = webdriver.PhantomJS()
		self.reader = maxminddb.open_database('GeoLite2-City.mmdb')
		self.headers = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'

	def get_country(self, ip):
		data = self.reader.get(ip)
		return data['country']['names']['en']

	def get_date(self, hours, minutes, seconds):
		date = datetime.now() - timedelta(hours = hours, minutes = minutes, seconds = seconds)
		return date.strftime('%m-%d-%Y %H:%M:%S')

	def modify_url(self, id):
		self.url = 'https://sockslist.net/proxy/server-socks-hide-ip-address/{}'.format(id)

	def check_cloudfare(self, ip, port, type):
		socks = 'socks{}://{}:{}'.format(type.split('/')[0], ip, port)
		proxies = {
			'http': socks,
			'https': socks
		}
		r = requests('https://medium.com', headers=self.headers, proxies=proxies)
		if 'captcha' in r.text:
			return '1'
		else:
			return '0'



proxy_data = []
flag = 1
pl = ProxyList()
while flag <= 3:
	pl.driver.get(pl.url)
	html = pl.driver.page_source
	soup = BeautifulSoup(html,'html.parser')
	row = soup.find('table', {'class': 'proxytbl'}).findAll('tr')
	for r in row:
		if r.find('td', {'class': 't_ip'}) is not None:
			ip = r.find('td', {'class': 't_ip'}).string
			port = format(r.find('td', {'class': 't_port'})).split('>')[4].strip().split('<')[0].strip()
			p_type = 'SOCKS' + r.find('td', {'class': 't_type'}).string.strip()
			hours = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[0])
			minutes = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[1])
			seconds = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[2])
			# cf = pl.check_cloudfare(ip, port, p_type)
			data = {
				'ip': ip,
				'port': port,
				'type': p_type,
				'country': pl.get_country(ip),
				'date': pl.get_date(hours, minutes, seconds),
				'source': 'sockslist.net',
				'tags': []#{'cfworking': cf}]
			}
			proxy_data.append(data)
	with open('socks_list.json', 'a') as f:
		# f.write(format(proxy_data))
		json.dump(proxy_data, f, sort_keys=True, indent=4)
	flag += 1
	pl.modify_url(flag)
	




