#!env/bin/python

# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Command line interface for interacting with Toggl, using the official
# Toggl API. (https://www.toggl.com/public/api)
# end.
from toggl_cli.functions import *
import sys, os

menuStr = '''
=========================
Toggl CLI - Main Menu
=========================
1. Continue recent task
2. Continue recent time entry
3. New time entry
4. Exit
'''

def get_selection():
	# Get the description based on user input
	sys.stdout.write("Your selection: ")

	try:
		return int(getkey())  - 1
	except ValueError:
		exit("Invalid selection. Exiting...")

# Menu Loop!
while True:

	print menuStr
	response = get_selection() + 1
	print response

	# Continue recent task
	if response == 1:
		print "Getting recent Tasks..."
		entries = get_recent("tasks", ["name", "project", "id"])
		
		# If an empty list, there are no tasks. Just get outta here!
		if len(entries) == 0:
			print "ERROR:No tasks were found. Returning to main menu."
			continue

		print "Press the number of the Task you wish to continue..."
		print_entries(entries, "name")

		# Get selection and print for confirmation
		selection = get_selection()
		print selection + 1

		description = entries[selection]["name"]
		taskID = entries[selection]["id"]
		new_time_entry(description, taskID)


	# Continue recent time entry
	elif response == 2:
		print "Getting recent Time Entries..."
		entries = get_recent("time_entries", ["description", "project", "id"])
		print "Press the number of the Time Entry you wish to continue..."
		print_entries(entries, "description")

		# Get selection and print for confirmation
		selection = get_selection()
		print selection + 1

		description = entries[selection]["description"]
		new_time_entry(description)

	# New time entry
	elif response == 3:
		description = raw_input("\nWhat will you be working on?: ")
		new_time_entry(description)
	# Exit
	else:
		exit("Exiting...")

