# Author: Joseph McCullough (@joe_query, joseph@vertstudios.com)
# Functions for the toggl command line interface.

# Note for myself: Use "http://httpbin.org/post" when needed for testing.

import getpass, requests, simplejson, os, time, datetime
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


def get_data(key, params=None, data=None):
	'''
	Get data from API. See list of keys in the api function in
	this document.

	params: A dictionary that will be urlencoded

	Returns a dictionary.
	'''
	with session() as r:
		if params:
			response = r.get(api(key, params), data=data)
		else:
			response = r.get(api(key), data=data)

		content = response.content
		json = simplejson.loads(content)
		return json


def get_data_dict(apikey, datakey, dataValue):
	'''
	Output the dicionary of a specific datakey (such as 'name') with a
	value (such as 'My Weekend Project' for a given apikey 
	(such as 'projects')
	'''
	data = get_data(apikey)["data"]
	dump = simplejson.dumps(data, indent=2)

	# Data is an array of dicts. See if we find our datakey. If so,
	# return it. If not, return false.
	
	for x in data:
		if x[datakey].lower() == dataValue.lower():
			return x
	return False

def test_api(key, params=None, data=None):
	'''
	Output API info. Output wrapper for get_data
	'''
	print simplejson.dumps(get_data(key, params, data), indent=2)


def get_latest_time_entries():
	'''
	Gets the latest time entries. Returns a dictionary
	'''
	url = api("time_entries")
	with session() as r:
		content = r.get(url).content
		#print simplejson.loads(content) 

def new_time_entry(description):
	''' 
	Creates a new time entry. Pass in a description string.
	'''

	# Get the current time and store it. Then pause until the user
	# says they are finished timing the task. Get the time they stopped
	# the timer, subtract it from the start_time, and store the difference
	# in seconds as the duration.
	start_time = datetime.datetime.now()

	# Let user know to press enter to stop timer, and output dashes
	# for pretty formatting.
	# Output dashes for pretty formatting
	print ""
	print "Task: " + description
	print start_time.strftime("Started at: %I:%M%p GMT")
	print dashes(PROMPT + description)
	print "Press Enter to stop timer... (CTRL-C to cancel)"
	try:
		raw_input()
	except (KeyboardInterrupt, SystemExit):
		print "\nTask cancelled. Exiting."
		exit()

	print "Sending data..."

	end_time = datetime.datetime.now()
	time_difference = (end_time - start_time).seconds
	projectID = get_data_dict("projects", "name", TOGGL_PROJECT)["id"]

	# Data passed to the request
	data = {"time_entry":{
			"duration": time_difference,
			"start": start_time.isoformat(),
			"stop": "null",
			"created_with": "Python Command Line Client",
			"project": {"id":projectID},
			"description": description}}
	url = api("time_entries")
	#url = "http://httpbin.org/post"

	headers = {"Content-Type": "application/json"}

	# JSON Encode the data dict
	data=simplejson.dumps(data)
	with session(headers=headers) as r:
		response = r.post(url, data=data)
		#print response.content
		print "Success."

def dashes(string):
	'''
	Return a string of dashes the length of string. Just for pretty 
	formatting
	'''
	return "-" * len(string)


# Get the global variables and settings.
from global_vars import *
