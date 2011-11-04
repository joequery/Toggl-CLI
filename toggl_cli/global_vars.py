# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Global/Environment Variables and Settings

import os, time, getpass
from functions import get_settings_from_file

# Get project settings from ~/.toggl and local .toggl_project file
TOGGL = {}

'''
The following criteria must be met before me proceed:
	1. ~/.toggl must exist
	2. a .toggl_project must exist in the directory the script is called.
'''
# 1. ~/.toggl must exist
try:
	home = os.path.expanduser("~")
	fileLoc = os.path.join(home, ".toggl")
	get_settings_from_file(fileLoc, TOGGL)
except IOError:
	exit("Must have a ~/.toggl file...")

# 2. a .toggl_project must exist in the directory the script is called.
# This file can also overwrite any of the settings in ~/.toggl
try:
	projectFile = os.path.join(os.getcwd(), ".toggl_project")
	get_settings_from_file(projectFile, TOGGL)
except IOError:
	exit("Must have a .toggl_project file in this directory...")

# User has the option of not specifying a password in the ~/.toggl file
# for security concerns. If they didn't specify the password, ask for it
# now.
if "PASSWORD" not in TOGGL.keys():
	TOGGL["PASSWORD"] = getpass.getpass("Your password: ")

# API convenience vars
API_PREFIX = "https://www.toggl.com/api/v6/"
AUTH = (TOGGL["EMAIL"], TOGGL["PASSWORD"])

# Task prompt
PROMPT = "What are you working on?: "

# If project not specfied, inform user and exit
if "PROJECT" not in TOGGL.keys():
	print "A project must be specified. Exiting."
	exit()
