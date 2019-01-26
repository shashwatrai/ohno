import time
import os
import datetime
curr_time = time.time()
try:
	fptr =open(".timelog" ,"r")
except:
	fptr=open(".timelog","w")
	fptr.write(str(curr_time))
	print("Stopwatch started at " + str(datetime.datetime.now()))
else:
	if fptr:
		prev_time=fptr.read()
		prev_time=float(prev_time)
		print("Stopwatch ended at " + str(datetime.datetime.now()))
		print("Worked for ",curr_time-prev_time)
		os.remove(".timelog")