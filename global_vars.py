# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Global/Environment Variables and Settings

import os, time, getpass

# These environment variables are defined in ~/.toggl and are
# put into the environment by the bash wrapper

# Password may not be specified in file for security reasons.
try:
	TOGGL_PASSWORD = os.environ["TOGGL_PASSWORD"]
except KeyError:
	TOGGL_PASSWORD = getpass.getpass("Your password: ")

TOGGL_EMAIL = os.environ["TOGGL_EMAIL"]
cwd = os.environ["TOGGL_CALLDIR"]

# See if a .toggl_project file was specified. This file should just
# have the project name.
filePath = os.path.join(cwd, ".toggl_project")
projectFile = open(filePath, "r")
TOGGL_PROJECT = projectFile.read().strip()


API_PREFIX = "https://www.toggl.com/api/v6/"
AUTH = (TOGGL_EMAIL, TOGGL_PASSWORD)

PROMPT = "What are you working on?: "
'''
Begin Settings
'''
# Set the timezone
os.environ['TZ'] = "GMT"
time.tzset()

