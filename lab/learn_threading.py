import threading
import time
import datetime
import sys

EXIT_FLAG = 0

def run_timer():
	global EXIT_FLAG

	seconds = 0
	while EXIT_FLAG==0:
		time.sleep(1)
		timeFmt = datetime.timedelta(seconds=seconds)

		# Prevent extra write on exit
		if EXIT_FLAG == 0:
			sys.stdout.write("\r%s" % timeFmt)
			sys.stdout.flush()
			seconds += 1

def get_input():
	global EXIT_FLAG
	print "Press something!"
	raw_input()
	EXIT_FLAG = 1

inputThread = threading.Thread(target=get_input)
timerThread = threading.Thread(target=run_timer)

inputThread.start()
timerThread.start()
