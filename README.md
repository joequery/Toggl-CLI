# Toggl CLI

Although time tracking is an essential workflow tool, taking the time to click through a web app every time you start and stop a task is extremely annoying. The Toggl CLI (Command Line Interface) attempts to solve this issue by making it easy and fast to track your time.

## What is [Toggl](http://toggl.com)?
[Toggl](http://toggl.com) is a time tracking app that I absolutely love to use. The interface is simple and the time reports are extremely useful. Toggl's API powers this script.

## Usage
You'll need [python2.6](http://www.python.org/getit/releases/2.6/), [virtualenv](http://pypi.python.org/pypi/virtualenv), and [pip](http://pypi.python.org/pypi/pip) to complete the installation. Other 2.x versions of python will probably work, I just haven't tried them yet. After you install pip, do the following:

1. Download and extract the repo to wherever you want, as long as the toggl bash script is in your PATH. 
2. Rename and move "dottoggl.txt" to ~/.toggl, and edit the file to contain your account credentials. The script will ask you for your password at run time in the event you don't want to store your password in the file.
3. cd to the location where you extracted the repo. Execute the following to install the required packages:

		virtualenv env --python=python2.6
		. env/bin/activate
		pip install -r requirements.txt
		deactivate

4. Make yourself a project with the Toggl web app. cd to an appropriate directory for working on that project, and create a .toggl_project file in the directory, similar to the toggl_project_example.txt file located in the repo.

5. Now we're set! Make sure you're in your project directory with the .toggl_project file, and execute

		toggl "Your Task Description Here"

Press enter when you want to stop your task timer. You can immediately go check your Toggl dashboard and see the entry.

## Technologies Used
* [Requests](http://docs.python-requests.org/en/latest/index.html): HTTP for Humans
* [Toggl API](https://www.toggl.com/public/api)
