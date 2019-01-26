import os
import subprocess
import re
import sys
import requests
from bs4 import BeautifulSoup
import urllib
import tkinter as tk
import tkinter as ttk
from ans import *


GREEN = '\033[92m'
GRAY = '\033[90m'
CYAN = '\033[36m'
RED = '\033[31m'
YELLOW = '\033[33m'
END = '\033[0m'
UNDERLINE = '\033[4m'
BOLD = '\033[1m'

def confirm():
	option = {"yes": True, "y": True, "no": False, "n": False, "": True}

	while True:
		print(BOLD + YELLOW + "\nDo you want to search StackOverflow? [Y/N]   " + END, end='')
		choice = input().lower()
		if choice in option:
			return option[choice]

		print("Please respond with ('yes' or 'no') or ('y' or 'n').\n")

# returns compiler
def get_lang(File_Path):
	if File_Path.endswith(".py"):
		return "python3 "
	elif File_Path.endswith(".cpp"):
		return "g++ "
	elif File_Path.endswith(".java"):	
		return "javac "
	elif File_Path.endswith(".c"):
		return "gcc "
	elif File_Path.endswith(".js"):
		return "rhino "
	else: 
		return None 		
		
# prints help
def print_help():
	print("%sNAME%s\n\tOhno\n"%(BOLD,END))
	print("%sSYNOPSIS%s\n\t%sohno%s %s[%sfile_name]%s\n" % (BOLD, END,BOLD, END, YELLOW,UNDERLINE,END))
	print("\t%sohno%s -q %s[%scustom_query]%s\n"%(BOLD, END, YELLOW,UNDERLINE,END) )
	print("\t%sohno%s --query %s[%scustom_query]%s\n"%(BOLD, END, YELLOW,UNDERLINE,END) )
	print("\t%sohno%s -g %s[%scode_name]%s\n"%(BOLD, END, YELLOW,UNDERLINE,END) )
	print("\t%sohno%s --gfg %s[%scode_name]%s\n"%(BOLD, END, YELLOW,UNDERLINE,END) )
	print("\t%sohno%s -s %s[%scode_file]%s %s[%sinput_file]%s\n"%(BOLD, END, YELLOW,UNDERLINE, END, YELLOW, UNDERLINE,END) )
	print("\t%sohno%s --submit %s[%scode_file]%s %s[%sinput_file]%s\n"%(BOLD, END, YELLOW,UNDERLINE, END, YELLOW, UNDERLINE,END) )
	print("%sDESCRIPTION%s\n\t\n"%(BOLD,END))


def error_on_python(error):
	list_err = []
	if any(err in error for err in["KeyboardInterrupt", "SystemExit", "GeneratorExit"]):
		return None
	else:
		list_err.append(error.split('\n')[-2].strip())
		return list_err

def error_on_java(error):
	list_err = []
	length = len(error.split('\n'))
	for i in range(length):
		m = re.search(r'.*error:(.*)', error.split('\n')[i])
		if m:
			list_err.append(m.group(1).strip())
	return list_err

def error_on_cpp(error):
	list_err = []
	length = len(error.split('\n'))
	for i in range(length):
		m = re.search(r".*error:(.*)", error.split('\n')[i])
		if m:
			list_err.append(m.group(1).strip())
	for i in range(len(list_err)):
		list_err[i] = list_err[i][:list_err[i].find("(")]
		list_err[i] = list_err[i][:list_err[i].find("{")]
		list_err[i] = list_err[i][:list_err[i].find("[")]
	return list_err

def error_on_c(error):
	list_err = []
	length = len(error.split('\n'))
	for i in range(length):
		m = re.search(r".*error:(.*)", error.split('\n')[i])
		if m:
			list_err.append(m.group(1).strip())
	for i in range(length):
		m = re.search(r".*warning:(.*)", error.split('\n')[i])
		if m:
			list_err.append(m.group(1).strip())
	for i in range(len(list_err)):
		list_err[i] = list_err[i][:list_err[i].find("(")]
		list_err[i] = list_err[i][:list_err[i].find("{")]
		list_err[i] = list_err[i][:list_err[i].find("[")]
	return list_err

def error_on_js(error):
	list_err = []
	list_err.append(error.split('\n')[0][4:].strip())
	for i in range(len(list_err)):
		list_err[i] = list_err[i][:list_err[i].find("(")]
		list_err[i] = list_err[i][:list_err[i].find(":")+2]
		list_err[i] = list_err[i][:list_err[i].find("{")]
		list_err[i] = list_err[i][:list_err[i].find("[")]
	return list_err

def get_error(error, language):
	if error == "":
		return None
	elif language == "python3 ":
		return error_on_python(error)
	elif language == "javac ":
		return error_on_java(error)
	elif language == "g++ ":
		return error_on_cpp(error)
	elif language == "gcc ":
		return error_on_c(error)
	elif language == "rhino ":
		return error_on_js(error)
	else:
		return None

def execute(command):
	sp = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err=sp.communicate()
	return (out.decode('utf-8'), err.decode('utf-8'))

def scrap(errors_list):
	global stack_questions_list
	stack_questions_list = []
	for error in errors_list:
		params = {"q": error}
		error_next = urllib.parse.urlencode(params)
		url="https://stackoverflow.com/search?pagesize=3&"+error_next
		page=requests.get(url)
		html_doc=page.text
		soup=BeautifulSoup(html_doc,'lxml')
		all_a_tags_questions=soup.find_all('a',class_="question-hyperlink")
		all_stats_tags_for_answer=soup.find_all('div',class_=["c","status"])
		i=0
		for question in all_a_tags_questions:
			if i>=10:
				break
			stack_questions_list.append([(question.text).strip(),question['href']])
			i=i+1
		i=0
		for each_strong in all_stats_tags_for_answer:
			if i>=10:
				break
			each_strong.find('strong')
			stack_questions_list[i].append((each_strong.text).strip())
			i=i+1
	util(stack_questions_list)

language = get_lang(sys.argv[1])
command = language + sys.argv[1]

out, err = execute(command)
if out:
	print(out,end='')
if err:
	print(err,end='')
else:
	print(CYAN + BOLD + "\nNo errors detected" + END)
	quit()
all_error = []
if confirm():
	all_error.append(get_error(err, language))
	scrap(all_error[0])