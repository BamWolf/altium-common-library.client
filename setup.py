#-*- coding: utf-8 -*-

from distutils.core import setup
import sys
import py2exe



sys.argv.append('py2exe')

opts =	{
	"py2exe":	{
			'includes': ['decimal', 'datetime', 'sip'],
			'excludes' : [],
			'dll_excludes': ['msvcr71.dll', 'MSVCP90.dll'],
			'packages': ['modules'],
			'bundle_files': 2,
			'dist_dir': '../exe',
			'compressed': True
			}
	}

print opts


setup	(
	name = 'Crowd Library Component Wizard',
	version = '0.3',
	description = '<Description>',
	author = 'Jack Krieger',

#	console = ['wizard.py'],
	windows = ['wizard.py'],
	options = opts,
	zipfile = None
	)
