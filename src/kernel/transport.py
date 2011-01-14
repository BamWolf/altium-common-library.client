#-*- coding: utf-8 -*-

import urllib
import urllib2

# connection
defaultgeturl = 'http://noxius.ru/index2.php'
defaultseturl = 'http://noxius.ru/index2.php'


def send(application, xmldata):
	proxydata = {}
	for option in ('user', 'pass', 'host', 'port'):
		proxydata[option] = application.settings.option('PROXY', option)

	proxydata['port'] = int(application.settings.option('PROXY', 'port') or 0)

	print proxydata

	if proxydata['host']:
		proxy_support = urllib2.ProxyHandler({"http" : "http://%(user)s:%(pass)s@%(host)s:%(port)d" % proxydata})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)

	data = urllib.urlencode({'xml': xmldata})

	try:
#		urldata = urllib2.urlopen(application.settings.option('CONNECTION', 'set url', defaultseturl, True), data).read()
		urldata = 'urldata'

		#херня вместо адреса
		#<urlopen error [Errno 11004] getaddrinfo failed>

		#левый порт
		#<urlopen error [Errno 10049] The requested address is not valid in its context>

	except urllib2.HTTPError, e:
		# неправильный адрес
		#HTTP Error 407: Proxy Authentication Required
		print 'yes'
		print e
#		application.exit()

	except urllib2.URLError, e:
		# нет инета (сетевого подключения)
		print e
#		application.exit()

	print urldata

	with (open('data/answer.xml', 'wb')) as xmlfile:
		xmlfile.write(urldata)

	return urldata

