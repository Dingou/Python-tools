#!/usr/bin/env python
import time
import os,sys,boto3
import configparser
import logging
from daemon import Daemon
from dateutil.tz import *
from datetime import *
'''
This script is for testing

'''

'''
AWS RDS get CREDENTIALS from /etc/zabbix/.rds
'''
AWS_CREDENTIALS_FILE = '/etc/zabbix/.rds'

'''
Get access KEY for rds
'''
def check_rds_credentials():
    rds_access = {}
    try:
        if os.path.exists(AWS_CREDENTIALS_FILE):
            cfg = configparser.RawConfigParser()
            cfg.read(AWS_CREDENTIALS_FILE)
            rds_access = {
                'aws_access_key_id': cfg.get('rds','aws_access_key_id'),
                'aws_secret_access_key': cfg.get('rds','aws_secret_access_key'),
                'region_name': cfg.get('rds','region')
            }
        else:
            print 'Config file not found!'
            sys.exit(1)
    except:
        print 'Error reading config file!'
        sys.exit(1)
    return rds_access


class rdsevents_daemon(Daemon):
    def __init__(self,aws_access,Duration,pidfile,logfile,logname):
        Daemon.__init__(self,pidfile,logfile,logname)
        self.aws_access = aws_access
        self.Duration = Duration

    def des_rdsevents(self):
        logger = self._set_logging()
        client = boto3.client('rds', **self.aws_access)
        while True:
            responses = client.describe_events(Duration=self.Duration)
            for response in responses['Events']:
                logger.info(
                    "DATE: %(Date)s\n"
                    "Message: %(Message)s\n"
                    "EventCategories: %(EventCategories)s\n"
                    "SourceIdentifier : %(SourceIdentifier)s\n"
                    "SourceType: %(SourceType)s\n" %response)
            time.sleep(300)


    def _run(self):
        self.des_rdsevents()

if __name__ == "__main__":
    rds_access = check_rds_credentials()
    daemon = rdsevents_daemon(aws_access=rds_access,Duration=int(5),pidfile='/tmp/rdsevents.pid',logfile='/tmp/rdsevents.log',logname='RDS_EVENTS_LOG')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]