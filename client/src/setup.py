#-*- coding: utf-8 -*-

from distutils.core import setup
import sys
import py2exe


if __name__ == '__main__':

	if 'debug' in sys.argv:
		CONSOLE = [{'script': 'wizard.py', 'icon_resources': [(0, 'wizard.ico')]}]
		WINDOWS = []
		sys.argv.remove('debug')

	else:
		CONSOLE = []
		WINDOWS = [{'script': 'wizard.py', 'icon_resources': [(0, 'wizard.ico')]}]

	OPTIONS = {'py2exe': {
			'includes': ['decimal', 'datetime', 'sip'],
			'excludes' : [],
			'dll_excludes': ['msvcr71.dll', 'msvcp90.dll'],
			'packages': ['pyodbc'],
			'bundle_files': 2,
			'dist_dir': '../release',
			'compressed': True
			}
		}

	setup (
		name = 'Altium Common Library Wizard',
		version = '0.3',
		description = '<Description>',
		author = 'Jack Krieger',
	
		console = CONSOLE,
		windows = WINDOWS,
#		data_files = [('imageformats', ['qico4.dll'])],
		options = OPTIONS,
		zipfile = None
		)
