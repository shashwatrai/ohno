# from subprocess import Popen, PIPE, STDOUT

# cmd=['echo','history']
# e = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
# output = e.communicate()
# print(output)
import os
p = os.system('fc -ln')  
# print(p.read()) 