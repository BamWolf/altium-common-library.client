#-*- coding: utf-8 -*-

from distutils.core import setup
import sys
import py2exe

sys.argv.append('py2exe')

opts =	{
	"py2exe":	{
			'includes': 'decimal, datetime, sip',
			'excludes' : [],
			'dll_excludes': ['msvcr71.dll', 'MSVCP90.dll'],
			'packages': 'modules',
			'bundle_files': 2,
			'dist_dir': '../exe',
			'compressed': True
			}
	}

print opts


setup	(
	name = 'PyClient',
	version = '0.2',
	description = '<Description>',
	author = 'Jack Krieger',

	console = ['pyclient2.py'],
	options = opts,
	zipfile = None
	)
