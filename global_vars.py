# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Global/Environment Variables and Settings

import os, time, getpass
from functions import get_project_file_settings,print_dict

# Some environment variables are defined in ~/.toggl and are
# put into the environment by the bash wrapper
TOGGL = {}

# Password may not be specified in file for security reasons.
try:
	TOGGL["PASSWORD"] = os.environ["TOGGL_PASSWORD"]
except KeyError:
	TOGGL["PASSWORD"] = getpass.getpass("Your password: ")

TOGGL["EMAIL"] = os.environ["TOGGL_EMAIL"]
cwd = os.environ["TOGGL_CALLDIR"]


# API convenience vars
API_PREFIX = "https://www.toggl.com/api/v6/"
AUTH = (TOGGL["EMAIL"], TOGGL["PASSWORD"])

# Task prompt
PROMPT = "What are you working on?: "

# Get project settings from .toggl_project file
PROJECT_FILE = open(os.path.join(cwd, ".toggl_project"), "r")
settings = get_project_file_settings(PROJECT_FILE)

# Merge the settings dictionary with the TOGGL dictionary
TOGGL = dict(TOGGL.items() + settings.items())

# If project not specfied, inform user and exit
if "PROJECT" not in TOGGL.keys():
	print "A project must be specified. Exiting."
	exit()
