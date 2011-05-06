#-*- coding: utf-8 -*-

import os
import sys
import csv

from kernel.abstract import AppException
from kernel.utils import OptionManager

#from kernel import i18n


######################################

def _(s):
	return s


class CSVExporter():
	name = 'csv'

	def __init__(self):
		self.settings = OptionManager('csv.ini')

		if not self.settings.option('SETTINGS', 'outputpath'):
			raise AppException(_('no output path'))


	def set(self, data):
		if not data:
			raise AppException(_('no data to save'))

		for category in data:
			filename, columns, elements = data[category]

			csvfilename = os.path.abspath(os.path.join(self.settings.option('SETTINGS', 'outputpath'), '.'.join((filename, 'csv'))))
			print
			print _('updating %s') % (csvfilename,)

			encoding = self.settings.option('SETTINGS', 'encoding') or 'utf-8'

			#if not encoding in encodings:
			#	return

			try:
				with open(csvfilename, 'wb+') as output:
					writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

					writer.writerow(columns)

					for element in elements:
						writer.writerow([element[column].encode(encoding) for column in columns])

			except IOError, e:
				raise AppException(e)


