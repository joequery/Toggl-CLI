# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Command line interface for interacting with Toggl, using the official
# Toggl API. (https://www.toggl.com/public/api)
# The user should have a ~/.toggl file that exports
# TOGGL_EMAIL and TOGGL_PASSWORD. Remember that TOGGL has no 'E' at the 
# end.
from functions import *
import sys

# Allow the user to call this script through 'toggl "Decription Here"'
# or just toggl and specify it via prompt.
if len(sys.argv) > 1:
	description = sys.argv[1]
else:
	description = raw_input(PROMPT)

new_time_entry(description)
