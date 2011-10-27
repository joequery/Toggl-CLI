# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Command line interface for interacting with Toggl, using the official
# Toggl API. (https://www.toggl.com/public/api)
# end.
from functions import *
import sys, os

'''
The following criteria must be met before me proceed:
	1. ~/.toggl must exist
	2. a .toggl_project file may exist where the script is executed.
'''
# 1. ~/.toggl must exist
try:
	home = os.path.expanduser("~")
	f = open( os.path.join(home, ".toggl"))
except IOError:
	exit("Must have a ~/.toggl file...")


	

# Allow the user to call this script through 'toggl "Decription Here"'
# or just toggl and specify it via prompt.
if len(sys.argv) > 1:
	description = sys.argv[1]
else:
	description = raw_input(PROMPT)

new_time_entry(description)
