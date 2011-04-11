#-*- coding: utf-8 -*-

import urllib
import urllib2

from kernel import objects
#import objects

class HTTPClient():
	def __init__(self, url=None, proxy={'host': None}):
		self.url = url
		self.proxy = proxy



	def request(self, xmldata=None, values={}, headers={}):
		if not isinstance(xmldata, basestring):
			raise TypeError, 'string expected!'

		with (open('debug/query.xml', 'wb')) as xmlfile:
			xmlfile.write(xmldata)

		proxydata = self.proxy
		proxydata['port'] = int(proxydata['port'] or 0)

		print proxydata

		if proxydata['host']:
			proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxydata})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)

		values['form[value1]'] = xmldata

		body = urllib.urlencode(values)
		headers = {'User-Agent' : 'CrowdClient 0.4'}
		request = urllib2.Request(self.url, body, headers)


		print body

		try:
			response = urllib2.urlopen(request)

		except urllib2.HTTPError, e:
			# неправильный адрес
			#HTTP Error 407: Proxy Authentication Required
			print 'TRANSPORT ERROR:'
			print e.code
			return

		except urllib2.URLError, e:
			print 'TRANSPORT ERROR:'
			print e.reason
			#левый порт
			#<urlopen error [Errno 10049] The requested address is not valid in its context>

			#таймаут
			#<urlopen error [Errno 11006]>

			#херня вместо адреса
			#<urlopen error [Errno 11004] getaddrinfo failed>
			return


		urldata = response.read()

#		print urldata

		with (open('debug/answer.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata



if __name__ == '__main__':

# http://altiumlib.noxius.ru/?page=client&rem=read

	pr = {'host': '127.0.0.1', 'port': '3128', 'user': '', 'pass': ''}

	i = HTTPClient('http://altiumlib.noxius.ru/?page=client&rem=read', pr)

#	val = {'page': 'client', 'rem': 'read'}

	ans = i.request('<query/>')

	print ans