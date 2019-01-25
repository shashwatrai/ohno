import os
import subprocess
import re
import sys
import requests
from bs4 import BeautifulSoup
import urllib
import json


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
	return list_err

def error_on_js(error):
	list_err = []
	list_err.append(error.split('\n')[0][4:].strip())
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