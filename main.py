#!/usr/bin/env python
import requests

url_pre = "http://forum.anidub.com/topic/"
url_post = "/page__st__%d"

with open("data.txt") as tread_list:
	global url_list
	url_list = []
	for line in tread_list:
		url_list.append(url_pre + (line[:-1] if line[-1] == "\n" else line) + url_post)

print(url_list)