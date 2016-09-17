#!/home/django/py3env/bin/python
# coding: utf-8

from pprint import pprint
import re
import requests
from pprint import pprint

# Solve InsecureRequestWarning: Unverified HTTPS request is being made
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

station_dict = {}

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'

content = requests.get(url, verify=False)

stations = re.findall(r'([A-Z]+\|[a-z]+)', content.text)

for station in iter(stations):
    station_dict[station.split('|')[1]] = station.split('|')[0]

pprint(station_dict, indent=4)
