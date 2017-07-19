#!/usr/bin/env python
import config

import progressbar
import re
import requests
import time

from bs4 import BeautifulSoup
from lxml import html

config.__target_user_id = 48488

def save_db(data_base):
	with open("results.txt", "a") as db:
		for item in data_base:
			db.write("%s\n" % item)
		db.close()


def read_url_list():
	tread_list = open("data.txt", "r")
	url_list = []
	for line in tread_list:
		line = line[:-1] if line[-1] == "\n" else line
		url_list.append(line)
	tread_list.close()
	# url_list.sort()
	url_list = tuple(url_list)
	return url_list


def auth(a_url, a_data):
	s = requests.Session()
	s.post(a_url, a_data, headers=config.__headers)
	return s

def rate(session, post_id):
	res = session.get(config.__rate_system_url % (int(post_id)), headers=config.__headers)
	# print(res.status_code) # Временно
	return res


url_list = read_url_list()
auth_session = auth(config.__login_url, config.__login_data)
data_base = []

# rate(auth_session, 1153978)
# exit()

for I in range(0, len(url_list)):
	buff = ""
	str_numb = 1
	coutner = 0
	common_url_template = config.__url_pre + url_list[I] + config.__url_post

	bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
	print("Рабоатем с", url_list[I])
	bar.update(0)

	while True:
		common_url = common_url_template % (20 * (str_numb - 1))
		response = requests.get(common_url, headers=config.__headers)
		soup = BeautifulSoup(response.text, "lxml")

		posts = soup.find("div", {"id" : "ips_Posts"})
		if posts == buff:
			break

		# Искать id
		post_list = posts.find_all("div", {"class": "post_block"})
		listn = 1
		for item in post_list:
			try:
				if item.find("h3", {"class" : "guest"}):
					continue
				author_id = item.find("span", {"class" : "author"}).find("a").get("hovercard-id")
				if int(author_id) == config.__target_user_id:
					coutner += 1
					post_id = item.get("id")
					post_id = re.sub(r"post_id_", "", post_id)
					data_base.append(post_id)
					# rate(auth_session, post_id)
			except:
				print("Fail!", "Error in thread '%s' list '%d' count '%d'." % (url_list[I], listn, coutner))
			finally:
				listn += 1

		buff = posts
		time.sleep(0.05)
		bar.update(str_numb)
		str_numb += 1
	save_db(data_base)
	data_base = []
	print("\nГотово!", coutner, "\n")
	del bar



# Выделить обход в отдельную функцию search(url_list)
# Убрать авторизацию из обхода: она нужна только для оценивания
# Если url_list не задан, обходить весь форум.

# Доработать условие прекращение обхода треда
# Придумать, как обойти ограничение на кол-во минусов в день

# Добавить автореконнект при ошибке соединения.