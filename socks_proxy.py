
import json
import maxminddb
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta

class ProxyList():
	
	def __init__(self):
		self.url = 'https://sockslist.net/proxy/server-socks-hide-ip-address/'
		self.driver = webdriver.PhantomJS()
		self.reader = maxminddb.open_database('GeoLite2-City.mmdb')

	def get_country(self, ip):
		data = self.reader.get(ip)
		return data['country']['names']['en']

	def get_date(self, hours, minutes, seconds):
		date = datetime.now() - timedelta(hours = hours, minutes = minutes, seconds = seconds)
		return date.strftime('%m-%d-%Y %H:%M:%S')

	def modify_url(self, id):
		self.url = 'https://sockslist.net/proxy/server-socks-hide-ip-address/{}'.format(id)



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
			p_type = r.find('td', {'class': 't_type'}).string.strip()
			hours = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[0])
			minutes = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[1])
			seconds = int(r.find('td', {'class': 't_checked'}).string.strip().split(':')[2])
			data = {
				'ip': ip,
				'port': port,
				'type': p_type,
				'country': pl.get_country(ip),
				'date': pl.get_date(hours, minutes, seconds)
			}
			print data
			proxy_data.append(data)
	with open('socks_list.json', 'a') as f:
		# f.write(format(proxy_data))
		json.dump(proxy_data, f, sort_keys=True, indent=4)
	flag += 1
	pl.modify_url(flag)
	




