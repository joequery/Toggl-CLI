import threading
import time
import datetime
import sys

EXIT_FLAG = 0

def run_timer(theThread):
	'''
	Displays a timer that counts up while theThread is active
	theThread is a thread waiting on user input to stop the timer.
	'''

	seconds = 0
	while theThread.is_alive():
		timeFmt = datetime.timedelta(seconds=seconds)

		# Prevent extra write on exit
		if theThread.is_alive():
			sys.stdout.write("\r%s" % timeFmt)
			sys.stdout.flush()
			seconds += 1
			time.sleep(1)

def get_input():
	print "Press something!"
	raw_input()

inputThread = threading.Thread(target=get_input)
timerThread = threading.Thread(target=run_timer, args=(inputThread,))

inputThread.start()
timerThread.start()
