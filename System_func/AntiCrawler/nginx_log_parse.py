# -*- coding: utf-8 -*-
#    Copyright (c) 2017 Feng Shuo
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0


from itertools import islice
from config import RequestInfo
import re

__all__ = ['NginxRequestInfo', ]


class NginxLogParse(object):
    """
    Parse Nginx access.log into certain request info
    """

    __slots__ = ('_ngx_log', 'ngx_log',)

    def __init__(self):
        self._ngx_log = '/var/log/nginx/access.log'

    @property
    def ngx_log(self):
        """
        ngx_log filename
        :returns: ngx_log filename
        :rtype: ``string``
        """
        return self._ngx_log

    @ngx_log.setter
    def ngx_log(self, nginx_log):
        """
        set ngx_log
        """
        self._ngx_log = nginx_log

    def get_ngx_logs(self, line_nums=-1000):
        """
        Get nginx logs by line_nums

        :param line_nums:
        line/row number in nginx log
        :type line_nums:
        ``integer``
        :returns:
        if line_nums > 0, then get single request message line
        if line_nums = 0, get all request messages lines
        if line_nums < 0, get latest ${line_nums} request messages lines
        :rtype:
        ``list``
        """
        try:
            with open(self.ngx_log) as F:
                if line_nums > 0:
                    for line in islice(F, line_nums-1, line_nums):
                        return [line]
                else:
                    lines = F.readlines()[line_nums:]
                    return lines
        except Exception as e:
            print "Failed to get detail log(s) in nginx access.log due to %s" % e

    @staticmethod
    def ngx_log_to_requestinfo(log=None):
        """
        Parse nginx request log(one row/line) into namedtuple instance ``Request_info`` defined in class
        :param log:
        one nginx request log log in access.log you extracted
        :type log:
        string
        """
        # pat is defined due to default nginx access.log format
        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'
               '\[(.+)\]\s'
               '"GET\s(.+)\s\w+/.+"\s'
               '(\d+)\s'
               '(\d+)\s'
               '"(.+)"\s'
               '"(.+)"'
               )
        if log:
            request_info = re.findall(pat, log)[0]
            if request_info:
                request_info = RequestInfo(request_info[0], request_info[1], request_info[2], request_info[3],
                                           request_info[4], request_info[5], request_info[6])
                return request_info

# TODO should move to test
#ngx_request_info = NginxLogParse()
#ngx_request_info.ngx_log = '../test.log'
#line = ngx_request_info.get_ngx_logs(100)
#req_info = ngx_request_info.ngx_log_to_requestinfo(line[0])
#