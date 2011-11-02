# Toggl CLI

Although time tracking is an essential workflow tool, taking the time to click through a web app every time you start and stop a task is extremely annoying. The Toggl CLI (Command Line Interface) attempts to solve this issue by making it easy and fast to track your time.

## What is [Toggl](http://toggl.com)?
[Toggl](http://toggl.com) is a time tracking app that I absolutely love to use. The interface is simple and the time reports are extremely useful. Toggl's API powers this script.

## Installation and Configuration
Toggl CLI requires [python](http://www.python.org/). After you install python, execute the following:

		git clone git://github.com/joequery/Toggl-CLI.git
		cd Toggl-CLI
		sudo python setup.py install

Now edit the ~/.toggl file created for you and fill it in with your
credentials. Note that entering your password into this file is optional. If you don't, the script will request it at runtime. 


## Usage
1. Create a new [Toggl Project](https://www.toggl.com/projects) via the web app.
2. In the directory you plan on working in, create a .toggl_project file similar to the [toggl_project_example.txt file](https://github.com/joequery/Toggl-CLI/blob/master/toggl_project_example.txt). Specify a Project and optionally a Client in this file.

Now simply execute

	/your/project/directory$ toggl

	----------------------
	Toggl CLI
	----------------------
	1. Continue recent task
	2. Continue recent time entry
	3. New time entry
	4. Exit

	Your selection: 

You will be prompted with a menu. You can continue a recent task, continue a recent time entry, or start a completely new time entry with your own description.

After you make your selections from the menu, pressing enter will stop the timer and send the time to Toggl. Pressing CTRL+C will cancel the timer and NOT send the time to Toggl. This is useful in the event you get distracted or forget your timer is running!

You can immediately go check your Toggl dashboard and see the entry.

## Technologies Used
* [Requests](http://docs.python-requests.org/en/latest/index.html): HTTP for Humans
* [Toggl API](https://www.toggl.com/public/api)
