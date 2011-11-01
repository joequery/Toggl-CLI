# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Functions for the toggl command line interface.

# Note for myself: Use "http://httpbin.org/post" when needed for testing.

import getpass, requests, os, time, datetime, sys, select, termios, tty
from itertools import groupby

# Resolve simplejson discrepancy
try: import simplejson
except ImportError: import json as simplejson

from urllib import urlencode

def api(key, params=None):
	'''
	Return the API url call. 
	Potential keys:
		me
		time_entries
		workspaces
		clients
		projects
		tasks
		tags
		users

	For more info, see https://www.toggl.com/public/api

	params is a dictionary of key value pairs
	'''

	if params:
		apiCall =  API_PREFIX + key + ".json?" + urlencode(params)
	else:
		apiCall =  API_PREFIX + key + ".json"
	return apiCall

def session(headers=None):
	'''
	Session wrapper for convenience
	'''
	if headers:
		return requests.session(auth=AUTH, headers=headers)
	else:
		return requests.session(auth=AUTH)


def get_data(key):
	'''
	Get data from API. See list of keys in the api function in
	this document.
	
	'''
	with session() as r:
		response = r.get(api(key))

		content = response.content
		if response.ok:
			json = simplejson.loads(content)["data"]

			# Reverse the list to get correct chronological order. Also,
			# remove duplicates. But make sure this is actually a list!
			if type(json) is list:
				json.reverse()
			return json
		else:
			exit("Please verify your login credentials...")

def send_data(key, params=None, data=None):
	'''
	Use the api to send data.

	params: A dictionary that will be urlencoded

	Returns a dictionary.
	'''
	headers = {"Content-Type": "application/json"}

	# JSON Encode the data dict
	data=simplejson.dumps(data)
	with session(headers=headers) as r:
		response = r.post(api(key), data=data)

		content = response.content
		if response.ok:
			json = simplejson.loads(content)
			return json["data"]
		else:
			exit("Please verify your login credentials...")


def get_data_where(api, dataPair):
	'''
	Output the dicionary of a specific datakey (such as 'name') with a
	value (such as 'My Weekend Project' for a given apikey 
	(such as 'projects')
	'''
	data = get_data(api)
	dump = simplejson.dumps(data, indent=2)

	# We'll append to this list and return it
	returnList = []

	# Change data type so we can iterate
	dataPair = dataPair.items()[0]

	# Data is an array of dicts. See if we find our datakey. If so,
	# return it. If not, return false.
	
	for x in data:
		if dataPair in x.items():
			returnList.append(x)
	return returnList

def test_api(key):
	'''
	Output API info. Output wrapper for get_data
	'''
	print_dict(get_data(key), indent=2)


def get_recent(apikey, keyList, numEntries=9):
	'''
	Gets the latest instances of apikey that corresponds to the current
	project. 

	keyList: List of keys you want to extract from the api call. 
	numEntries: Number of entries to get.

	ex: get_recent("time_entries") returns recent time entries 
	for the project.

	'''
	project = get_project(small=True)
	entries = get_data_where(apikey, {"project":project})

	# Remove duplicates
	recent = remove_dups(entries, "description")
	return recent[0:numEntries]
		
def print_entries(entries, description, numToPrint=10):
	'''
	Pretty print entries. Since some api calls have the description as 
	"description" and others have it as "name", we'll need to specify it
	'''

	# Ew, a bunch of string formatting
	strLength = 60 
	counter = 1
	maxCounterLen = len(str(numToPrint)) + 2
	width = str(strLength + maxCounterLen)
	fmtString = "{0:<%s}{1:<%s}" % (maxCounterLen, width)

	for x in entries[0:numToPrint]:
		counterLen = len(str(counter))
		d = x[description].strip()
		if len(d) >= strLength - 3:
			d = d[0:strLength-3] + "..."

		p = x["project"]["client_project_name"]
		print fmtString.format(str(counter) + ".", d)
		counter += 1

def new_time_entry(description, taskID=False):
	''' 
	Creates a new time entry. Pass in a description string.
	If this is a task (the PRO feature), set task to True. 
	'''

	# Get the project ID of the client/project pair specified in 
	# .toggl_project. Make sure it's valid now before they start the timer
	# or they'll waste time in the event it's invalid
	try:
		projectID = get_project()["id"]
	except TypeError:
		if "CLIENT" in TOGGL.keys():
			print "The project " + TOGGL["PROJECT"]+" under the client " +\
			TOGGL["CLIENT"] + " was not found."
		else:
			print "The project " + TOGGL["PROJECT"] + " was not found"
		exit("Exiting...")
					


	# Get the current time and store it. Then pause until the user
	# says they are finished timing the task. Get the time they stopped
	# the timer, subtract it from the start_time, and store the difference
	# in seconds as the duration.
	#start_time = datetime.datetime.now()
	start_time = datetime.datetime.utcnow()
	local_start_time = datetime.datetime.now()

	# Let user know the timer has started, and wait for them to press
	# Enter to stop it.
	timer_start_print(description, local_start_time)

	try:
		raw_input()
	except (KeyboardInterrupt, SystemExit):
		exit("Task cancelled. Exiting")

	print "Sending data..."

	end_time = datetime.datetime.utcnow()
	time_difference = (end_time - start_time).seconds


	# Data passed to the request
	data = {
			"duration": time_difference,
			"start": start_time.isoformat(),
			"stop": "null",
			"created_with": "Python Command Line Client",
			"project": {"id":projectID},
			"description": description}

	# If task Id was specified, add it to the data dict
	if taskID:
		data["task"] = {"id":taskID}

	# Add to time_entry key
	data = {"time_entry" : data }


	send_data("time_entries", data=data)
	print "Success."

def dashes(string):
	'''
	Return a string of dashes the length of string. Just for pretty 
	formatting
	'''
	return "-" * len(string)

def print_dict(theDict, indent=4):
	'''
	Outputs a dictionary all pretty like
	'''
	print simplejson.dumps(theDict, indent=indent)

def parse_file(fileLoc):
	'''
	Return a list containing the lines of the file.
	Ignore commented lines (lines beginning with #)

	fileLoc: location of the file as a string
	'''
	handle = open(fileLoc)

	# We'll be returning this list.
	returnList = []

	for line in handle:
		li = line.strip()

		# Ignore empty lines and comments
		if li and not li.startswith("#"):
			returnList.append(li)
	return returnList

def get_settings_from_file(keyList, fileLoc, theDict):
	'''
	parses file at fileLoc and searches for key:value pairs specified
	by keyList.

	Alters theDict dictionary 
	'''
	fileContents = parse_file(fileLoc)
	for line in fileContents:
		# Store the key value pair. Uppercase Key since it will be 
		# used in a global variable
		tmp = line.split(":")
		key = tmp[0].strip().upper()

		# Only append the key value pair if the key is found.
		if key in keyList:
			value = tmp[1].strip()
			theDict[key] = value

def timer_start_print(description, time):
	'''
	Print a message to let the user know that the timer has started
	and how to stop it
	'''
	
	print "\n"
	print "=" * 50
	print "Timer started!"
	print "=" * 50

	print "Task: " + description
	print "Project: " + TOGGL["PROJECT"]
	if "CLIENT" in TOGGL.keys():
		print "Client: " + TOGGL["CLIENT"]

	print time.strftime("Started at: %I:%M%p")
	print dashes(description)
	print "Press Enter to stop timer... (CTRL-C to cancel)"
	
def get_project(small=False):
	'''
	Get the dictionary of the project specified in the .toggl_project file.
	Will attempt to account for missing TOGGL["CLIENT"] key

	small as True returns a project dict containing only id, name,
	and client_project_name. Useful for passing as a parameter
	'''
	if "CLIENT" in TOGGL.keys():
		# It's stored Client - Project under the API
		tmp = TOGGL["CLIENT"] +" - "+ TOGGL["PROJECT"]
		project = get_data_where("projects", {"client_project_name":tmp})
	else:
		project = get_data_where("projects", {"name":TOGGL["PROJECT"]})
	
	# Should only be one response
	project = project[0]
	
	if small:
		return {"id":project["id"], 
				"name":project["name"], 
				"client_project_name": project["client_project_name"]}
	else:
		return project

def getkey():
	'''
	Get keystroke without having to press enter. *NIX only
	'''
	old_settings = termios.tcgetattr(sys.stdin)
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	answer = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	return answer

def remove_dups(theList, key):
	'''
	pass in a list of dictionaries theList and get back theList without
	duplicates

	See stackoverflow: http://bit.ly/tmwTIm 
	'''
	keyfunc = lambda d: (d[key])
	giter = groupby(sorted(theList, key=keyfunc), keyfunc)

	return [g[1].next() for g in giter]

# Get the global variables and settings.
from global_vars import *
