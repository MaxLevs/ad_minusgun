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

with open("data.txt") as tread_list:
	global url_list
	url_list = []
	for line in tread_list:
		buff = line[:-1] if line[-1] == "\n" else line
		url_list.append(__url_pre + buff + __url_post)
	tread_list.close()

url_list = tuple(url_list)

# Авторизация
s = requests.Session()
s.post(__login_url, __login_data)


data_base = []

buff = ""
str_numb = 1
bar = bar2 = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
while True:
	common_url = url_list[0] % (20 * (str_numb - 1))
	response = s.get(common_url, headers=__headers)

	if response.text == buff:
		print("Кончилось!!")
		break
	# Искать id
	with open("tests/" + str(str_numb) + "-resp.html", "w") as out:
		out.write(response.text)
		out.close()
	with open("tests/" + str(str_numb) + "-buff.html", "w") as out:
		out.write(buff)
		out.close()
	buff = response.text
	str_numb += 1
	time.sleep(0.05)
	bar.update(str_numb)
del bar