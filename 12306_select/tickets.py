#!/home/django/py3env/bin/python
# coding: utf-8
"""Train tickets query via command-line.

Usage:
    tickets.py [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets.py beijing shanghai 2016-08-25
"""
from docopt import docopt
from stations import stations
import requests
def cli():
    arguments = docopt(__doc__)
    from_staion = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_staion, to_station
    )
    print(url)
    r = requests.get(url, verify=False)
    print(r.json())
    #rows = r.json()['data']['datas']
    #print rows

if __name__ == "__main__":
    cli()
