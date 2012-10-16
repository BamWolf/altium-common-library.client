from setuptools import setup, find_packages

setup(
	name = "CSV",
	version = "0.1",
	description = """CSV Export Plugin""",
	author = 'Jack Krieger',
#	install_requires = [''],
	packages = ['csv_module'],
	entry_points = """
	[db.engine]
	instance = csv_module.csv_module:CSVExporter
	""")
