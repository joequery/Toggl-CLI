import threading
import datetime
from timer import run_timer

class ThreadClass(threading.Thread):
  def run(self):
	now = datetime.datetime.now()
	print "%s says Hello World at time: %s\n" % \
	(self.getName(), now)

for i in range(2):
  t = ThreadClass()
  t.start()

run_timer()

# I need to read this to learn about multithreaded programming:
# http://www.tutorialspoint.com/python/python_multithreading.htm
