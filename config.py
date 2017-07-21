import configparser
import requests
import sys

from fake_useragent import UserAgent
from os import path


__path_to_script = path.dirname(__file__)
__path_to_script = path.abspath(__path_to_script)

sys.setrecursionlimit(10000)
ua = UserAgent()
cp = configparser.ConfigParser()

__config_dir = "config"
__input_dir = "input"
__output_dir = "output"

auth_data = cp.read(path.join(__path_to_script, __config_dir, "auth.conf"))
config = cp.read(path.join(__path_to_script, __config_dir, "config.conf"))

# Если не существуют, бросить exaption

__url_root = cp.get("URL", "Root")
__rate_system_url = path.join(__url_root, cp.get("URL", "Rate"))
__url_pre = path.join(__url_root, "topic")
__url_post = "page__st__%d"

__headers = requests.utils.default_headers()
__headers.update({'User-Agent': ua.chrome})

__user_name = cp.get("Auth Data", "Login")
__user_password = cp.get("Auth Data", "Password")
__auth_key = cp.get("Auth Data", "AuthKey")

__login_url = path.join(__url_root, cp.get("URL", "login"))
__login_data = {
	"auth_key" : __auth_key, # Возможно, придется получать программно
	"referer" : __url_root,
	"ips_username" : __user_name,
	"ips_password" : __user_password,
	"rememberMe" : "1"
}