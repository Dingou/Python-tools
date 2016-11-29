import re
import json
import os
from urllib.request import urlopen

def getiploca(ipinfo):
    ip, count = ipinfo.split('\t')
    url = 'http://ipinfo.io/' + ip + '/json'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    report = '''
IP: %s
COUNT: %s
ORG: %s
CITY: %s
COUNTRY: %s
REGION: %s
\n
''' % (ip, count,  data['org'], data['city'], data['country'], data['region'])
    with open('ip.report', 'a') as ipreport:
        ipreport.write(report)

if __name__ == '__main__':
    with open('iplist.txt', 'r') as ipfile:
        ipinfolist = [ip.strip('\n') for ip in ipfile]
    try:
        os.remove('ip.report')
    except Exception as e:
        print("No File ip.report, continue...")
    finally:
        list(map(getiploca, ipinfolist))