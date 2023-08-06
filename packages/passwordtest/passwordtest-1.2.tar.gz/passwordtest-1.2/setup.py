from setuptools import setup, find_packages
import os, io

def Find_Packages():
	getdirectory = os.getcwd()
	fpath = os.path.join(getdirectory, 'passwordtest')
	fpath = fpath.replace("\\", "/")
	if os.path.exists(fpath):
		return ['passwordtest']
	else:
		return find_packages()
def README_MD():
	with open("README.md", 'r') as fh:
	 	longdescript = fh.read()
	return longdescript
__VERSION_TOOLS = "1.2"
mails = 'LCFHERSHELL@TUTANOTA.COM'.lower()
setup(
	name="passwordtest",
	version=__VERSION_TOOLS,
	description="Password security measurement tool",
	long_description=README_MD(),
	long_description_content_type="text/markdown",
	author="alfiandecker2",
	author_email=mails,
	packages=Find_Packages(),
	entry_points={
			'console_scripts': [
					'passwordtest = passwordtest.PassCLI:Mainprogram'
			]
	},
	python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
	zip_safe=False,
	keywords=["network", "MITM"]
	)
