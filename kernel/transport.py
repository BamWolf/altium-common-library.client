#-*- coding: utf-8 -*-

import urllib
import urllib2

from httplib import HTTP
from StringIO import StringIO
import urlparse

# elementtree (from effbot.org/downloads)
#from elementtree import ElementTree

from kernel import objects


class Transport():
	def __init__(self, application):
		self.session = None
		self.error = None
		self.settings = application.settings



	def send(self, xmldata=None, url=''):
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

#		urldata = urllib2.urlopen(url, data).read()

		try:
			urldata = urllib2.urlopen(url, data).read()

			#левый порт
			#<urlopen error [Errno 10049] The requested address is not valid in its context>

		except urllib2.URLError, e:
			#таймаут
			#<urlopen error [Errno 11006]>

			#херня вместо адреса
			#<urlopen error [Errno 11004] getaddrinfo failed>

			print 'TRANSPORT ERROR:', e
			return

		except urllib2.HTTPError, e:
			# неправильный адрес
			#HTTP Error 407: Proxy Authentication Required
			print 'TRANSPORT ERROR:', e
			return

		except urllib2.URLError, e:
			# нет инета (сетевого подключения)
			print 'TRANSPORT ERROR:', e
			return

		print urldata

		with (open('debug/answer.xml', 'wb')) as xmlfile:
			xmlfile.write(urldata)

		return urldata

class HTTP:

	user_agent = "HTTPClient (from effbot.org)"

	def __init__(self, uri):

		scheme, host, path, params, query, fragment = urlparse.urlparse(uri)
		if scheme != "http":
			raise ValueError("only supports HTTP requests")

		# put the path back together again
		if not path:
			path = "/"
		if params:
			path = path + ";" + params
		if query:
			path = path + "?" + query

		self.host = host
		self.path = path

	def do_request(self, body,
		# optional keyword arguments follow
		path=None, method="POST", content_type="text/xml",
		extra_headers=(), parser=None):

		if not path:
			path = self.path

		if isinstance(body, ElementTree.ElementTree):
			# serialize element tree
			file = StringIO()
			body.write(file)
			body = file.getvalue()

		# send xml request
		h = HTTP(self.host)
		h.putrequest(method, path)
		h.putheader("User-Agent", self.user_agent)
		h.putheader("Host", self.host)
		if content_type:
			h.putheader("Content-Type", content_type)
		h.putheader("Content-Length", str(len(body)))
		for header, value in extra_headers:
			h.putheader(header, value)
		h.endheaders()

		h.send(body)

		# fetch the reply
		errcode, errmsg, headers = h.getreply()

		if errcode != 200:
			raise Exception(errcode, errmsg)

		return ElementTree.parse(h.getfile(), parser=parser)
