from setuptools import setup, find_packages

setup(
	name = "MSACCESS",
	version = "0.1",
	description = """MS ACCESS Export Plugin""",
	author = 'Jack Krieger',
	install_requires = ['pyodbc'],
	packages = ['msaccess_module'],
	package_data = {'': ['*.pyd']},
	entry_points = """
	[db.engine]
	instance = msaccess_module.msaccess_module:MDBExporter
	""")
