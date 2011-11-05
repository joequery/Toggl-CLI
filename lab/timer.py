# A timer that prints into h:m:s

import time
import datetime
import sys

def run_timer():
	print "Timer Demonstration"

	seconds = 0
	while True:
		time.sleep(1)
		timeFmt = datetime.timedelta(seconds=seconds)
		sys.stdout.write("\r%s" % timeFmt)
		sys.stdout.flush()
		seconds += 1

	print ""
