#!/usr/bin/env python
import requests
import time
import progressbar
from bs4 import BeautifulSoup
from lxml import html

__target_user_id = 48488
__url_pre = "http://forum.anidub.com/topic/"
__url_post = "/page__st__%d"
__headers = {
	"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}
__user_name = "MaxLevs"
__user_password = "635241ml"
__login_url = "http://forum.anidub.com/index.php?app=core&module=global&section=login&do=process"
__login_data = {
	"auth_key" : "880ea6a14ea49e853634fbdc5015a024",
	"referer" : "http://forum.anidub.com/",
	"ips_username" : __user_name,
	"ips_password" : __user_password,
	"rememberMe" : "1"
}

def read_url_list():
	tread_list = open("data.txt", "r")
	url_list = []
	for line in tread_list:
		line = line[:-1] if line[-1] == "\n" else line
		url_list.append(line)
	tread_list.close()
	url_list.sort()
	url_list = tuple(url_list)
	return url_list

def auth(a_url, a_data):
	s = requests.Session()
	s.post(a_url, a_data)
	return s

url_list = read_url_list()
auth_session = auth(__login_url, __login_data)
data_base = []

for I in range(0, len(url_list)):
	buff = ""
	str_numb = 1
	bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
	print("Рабоатем с", url_list[I])
	bar.update(0)
	common_url_template = __url_pre + url_list[I] + __url_post
	while True:
		common_url = common_url_template % (20 * (str_numb - 1))
		response = auth_session.get(common_url, headers=__headers)

		soup = BeautifulSoup(response.text, "lxml")
		posts = soup.find("div", {"id" : "ips_Posts"})
		if posts == buff:
			break

		# Искать id

		buff = posts
		time.sleep(0.05)
		bar.update(str_numb)
		str_numb += 1
	print("\nГотово!", I, "\n")
	del bar

