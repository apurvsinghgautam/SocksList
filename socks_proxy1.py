import os
import re
import json
import maxminddb
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta

class ProxyList():
	
	def __init__(self):
		os.environ['PATH']=os.environ['PATH'] + ':/opt/phantomjs-2.1.1-linux-x86_64/bin'
		self.url = 'https://www.socks-proxy.net/'
		self.driver = webdriver.PhantomJS()
		self.reader = maxminddb.open_database('GeoLite2-City.mmdb')
		self.headers = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'

	def get_country(self, ip):
		data = self.reader.get(ip)
		return data['country']['names']['en']

	def get_date(self, minutes):
		date = datetime.now() - timedelta(minutes = minutes)
		return date.strftime('%m-%d-%Y %H:%M:%S')

	def check_cloudfare(self, ip, port, type):
		socks = 'socks{}://{}:{}'.format(re.findall('[0-9]', type)[0], ip, port)
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
flag = 0
pl = ProxyList()
pl.driver.get(pl.url)
html = pl.driver.page_source
soup = BeautifulSoup(html,'html.parser')
row = soup.find('table', {'id': 'proxylisttable'}).findAll('tr')
for r in row:
	if len(r.findAll('td')) != 0:
		ip = r.findAll('td')[0].string
		port = r.findAll('td')[1].string
		p_type = r.findAll('td')[4].string
		minutes = int(r.find('td', {'class': 'hd'}).string.split(' ')[0])
		# cf = pl.check_cloudfare(ip, port, p_type)
		data = {
			'ip': ip,
			'port': port,
			'type': p_type,
			'country': pl.get_country(ip),
			'date': pl.get_date(minutes),
			'source': 'www.socks-proxy.net',
			'tags': []#{'cfworking': cf}]
		}
		proxy_data.append(data)
with open('socks_list.json', 'a') as f:
	json.dump(proxy_data, f, sort_keys=True, indent=4)

	




