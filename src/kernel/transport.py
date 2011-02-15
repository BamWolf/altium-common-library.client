#-*- coding: utf-8 -*-

import urllib
import urllib2

from kernel import objects

# connection
defaultgeturl = 'http://altiumlib.noxius.ru/client/read'
defaultseturl = 'http://altiumlib.noxius.ru/client/read'



class Transport():
	def __init__(self, application):
		self.session = None
		self.error = None
		self.settings = application.settings



	def send(self, xmldata=None, url=defaultseturl):
		if not xmldata:
			self.error = 'nothing to send'

		with (open('debug/query.xml', 'wb')) as xmlfile:
			xmlfile.write(xmldata)

		proxydata = {}
		for option in ('user', 'pass', 'host', 'port'):
			proxydata[option] = self.settings.option('PROXY', option)

		proxydata['port'] = int(self.settings.option('PROXY', 'port') or 0)

		print proxydata

		if proxydata['host']:
			proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxydata})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)

		data = urllib.urlencode({'form[value1]': xmldata})

		try:
			urldata = urllib2.urlopen(url, data).read()

			#херня вместо адреса
			#<urlopen error [Errno 11004] getaddrinfo failed>

			#левый порт
			#<urlopen error [Errno 10049] The requested address is not valid in its context>

			#таймаут
			#<urlopen error [Errno 11006]>

		except urllib2.HTTPError, e:
			# неправильный адрес
			#HTTP Error 407: Proxy Authentication Required
			print 'yes'
			print 'Transport:', e
#			application.exit()

		except urllib2.URLError, e:
			# нет инета (сетевого подключения)
			print 'Transport:', e
#			application.exit()

		print urldata

		with (open('debug/answer.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata

