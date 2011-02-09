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



	def authenticate(self):
		""" аутентификация на сервере """
		query = objects.QueryMessage('identify')
		query.add_value('login', u'user')
		query.add_value('password', u'user')
		xmldata = query.build()

		xmldata = self.send(xmldata, 'http://altiumlib.noxius.ru/?page=client&rem=read')

		response = objects.ResponseMessage(xmldata).parse()
		self.session = response.values['sessionid']

		return self.session

	def send(self, xmldata=None, url=defaultseturl):
		if not xmldata:
			self.error = 'nothing to send'

		with (open('data/query.xml', 'wb')) as xmlfile:
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
#			urldata = urllib2.urlopen(self.settings.option('CONNECTION', 'set url', defaultseturl, True), data).read()
			urldata = urllib2.urlopen(url, data).read()

			#херня вместо адреса
			#<urlopen error [Errno 11004] getaddrinfo failed>

			#левый порт
			#<urlopen error [Errno 10049] The requested address is not valid in its context>

		except urllib2.HTTPError, e:
			# неправильный адрес
			#HTTP Error 407: Proxy Authentication Required
			print 'yes'
			print e
#			application.exit()

		except urllib2.URLError, e:
			# нет инета (сетевого подключения)
			print e
#			application.exit()

		print urldata

		with (open('data/answer.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata

