from setuptools import setup, find_packages

setup(
	name = "MySQL",
	version = "0.2",
	description = """MySQL Plugin""",
	author = 'Jack Krieger',
	packages = ['foo2_plugin'],
	entry_points = """
	[db.engine]
	do = foo2_plugin.foo:MySQLPlugin
	""")
