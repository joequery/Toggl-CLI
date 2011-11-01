from setuptools import setup
import os, shutil

setup(name='Toggl CLI',
      version='1.0',
      description='Python Distribution Utilities',
      author='Joseph McCullough',
      author_email='joseph@vertstudios.com',
	  install_requires=['requests'],
	  packages = ['toggl_cli'],
      scripts=['toggl']
     )

# Copy .toggl to ~/.toggl if the file doesn't exist.
home = os.path.expanduser("~")
togglFile = os.path.join(home, ".toggl")

try:
	open(togglFile)
	print "~/.toggl file found."
except IOError:
	print "Creating ~/.toggl file..."
	shutil.copy( ".toggl", os.path.join(home, ".toggl") )
