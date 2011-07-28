#-*- coding: utf-8 -*-

from distutils.core import setup
import sys
import py2exe


if __name__ == '__main__':

	if 'debug' in sys.argv:
		CONSOLE = ['wizard.py']
		WINDOWS = []
		sys.argv.remove('debug')

	else:
		CONSOLE = []
		WINDOWS = ['wizard.py']

	OPTIONS = {'py2exe': {
			'includes': ['decimal', 'datetime', 'sip'],
			'excludes' : [],
			'dll_excludes': ['msvcr71.dll', 'msvcp90.dll'],
			'packages': [],
			'bundle_files': 2,
			'dist_dir': '../release',
			'compressed': True
			}
		}

	setup (
		name = 'OpenVault Component Wizard',
		version = '0.3',
		description = '<Description>',
		author = 'Jack Krieger',
	
		console = CONSOLE,
		windows = WINDOWS,
		options = OPTIONS,
		zipfile = None
		)
