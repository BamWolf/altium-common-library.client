#-*- coding: utf-8 -*-

from distutils.core import setup
import sys
import py2exe

sys.argv.append('py2exe')

opts =	{
	"py2exe":	{
			'includes': 'decimal, datetime',
			'excludes' : [],
			'dll_excludes': ['msvcr71.dll'],
			'packages': 'modules',
			'bundle_files': 2,
			'dist_dir': '../exe',
			'compressed': True
			}
	}

print opts


setup	(
	name = 'PyClient',
	version = '0.1',
	description = '<Description>',
	author = 'Jack Krieger',

	console = ['pyclient.py'],
	options = opts,
	zipfile = None
	)
