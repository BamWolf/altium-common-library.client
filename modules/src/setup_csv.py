from setuptools import setup, find_packages

setup(
	name = "CSV",
	version = "0.1",
	description = """CSV Plugin""",
	author = 'Jack Krieger',
#	install_requires = [''],
	packages = ['csv_writer'],
	entry_points = """
	[db.engine]
	instance = csv_writer.csvfile:CSVWriter
	""")
