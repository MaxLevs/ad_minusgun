#!/usr/bin/env python
import requests

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

N = 25
common_url = url_list[0] % (20 * (N - 1))
with requests.Session() as s:
	s.post(__login_url, __login_data)
	global r
	r = s.get(common_url, headers=__headers)

with open("test.html", "w") as output:
	output.write(r.text)
