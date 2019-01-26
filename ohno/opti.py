import requests
import re
from bs4 import BeautifulSoup
from ohno.gui2 import *

def answer_scrap_gfg(url):
	page=requests.get(url)
	html_doc=page.text
	soup=BeautifulSoup(html_doc,"lxml")
	new_soup=soup.find("a",href=re.compile("geeksforgeeks.org"))
	new_soup=new_soup['href']
	new_soup=new_soup[new_soup.find("q=")+2:]
	new_soup=new_soup[:new_soup.find("&")]
	page_ans=requests.get(new_soup)
	html_doc_ans=page_ans.text
	soup_ans_all=BeautifulSoup(html_doc_ans,"lxml")
	all_methods=soup_ans_all.find_all("div",class_="responsive-tabs")
	length=len(all_methods)
	soup_ans=all_methods[length-1]
	all_codes=soup_ans.find_all("td",class_="code")
	language_tags=soup_ans.find_all("h2",class_="tabtitle")

	languages=[]
	codes=[]

	for tags in language_tags:
		languages.append(tags.text)

	for current_code in all_codes:
		codes.append(current_code.get_text())

	#print(len(languages))
	util(languages,codes)

# answer_scrap_gfg("https://www.google.com/search?q=fibonacci+gfg")
