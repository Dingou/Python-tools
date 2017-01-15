# -*- coding: utf-8 -*-
from collections import namedtuple
import time
import concurrent.futures
import re

# Todo: 1. add service reload;
# Todo: 2. add __main__ function
# Todo: 3. optimize;
# Todo: 4. distribute get crawler ip in access.log(Or we can use ELK instead)
# Todo: 5. juge crawler by USER AGENTs


class CrawlerIps(object):
    """
    To get Crawler Ips by crawler behaviours which you could find in nginx access.log
    use __slots__ to limit property setter
    """

    __slots__ = ('crawler_limit_rlt', 'crawler_limit_his', 'ngx_log', 'white_list', 'behav_list', 'blk_conf',
                 '_crawler_limit_rlt', '_crawler_limit_his', '_ngx_log', '_white_list', '_behav_list', '_blk_conf',
                 '_max_wks', 'mks_wks', '_user_agents', 'user_agents')

    # Define Req_info and Crawler_limit name tuple
    # Crawler_limit(Line_limit:lines once to detect,
    #               Rate_limit:time_limit to define it is a crawler ip or not,
    #               Tm_gap_limit:should less than the gap limit)
    # Req_info(): you could find more info in method req_info() below

    Crawler_limit = namedtuple('Crawler_limit', ['Line_limit', 'Rate_limit', 'Tm_gap_limit'])
    Req_info = namedtuple('Req_info', ['IP', 'Datatime', 'Dir', 'Status', 'BandWidth', 'Referrer', 'UserAgent'])

    def __init__(self):
        """
        _crawler_limit_rlt: real time Crawler_limit list, you could use this to detect ip on real time
        _crawler_limit_his: historic Crawler_limit list, you could detect historic crawler ip
        _ngx_log: nginx access log
        _white_list: white list ips
        _behav_list: crawler behavious, e.g: spider always crawler '/airplanes/135181983123/',
                     so we add airplanes to list
        _

        """
        self._crawler_limit_rlt = [self.Crawler_limit(-500, 150, 1800), self.Crawler_limit(-1000, 300, 3600),
                                   self.Crawler_limit(-3000, 900, 10400)]
        self._crawler_limit_his = [self.Crawler_limit(-5000, 1000, 18000)]
        self._user_agents = []
        self._ngx_log = '/var/log/nginx/access.log'
        self._white_list = ['54.233', '172']
        self._behav_list = ['airplanes']
        self._blk_conf = './blockips.conf'
        # self._blk_conf = '/etc/nginx/conf.d/blockips.conf'
        self._max_wks = 1

    @property
    def user_agents(self):
        return self._user_agents

    @user_agents.setter
    def user_agents(self, user_agents):
        self._user_agents = user_agents

    @property
    def max_wks(self):
        return self._max_wks

    @max_wks.setter
    def max_wks(self,max_workers):
        self._max_wks = max_workers

    @property
    def crawler_limit_rlt(self):
        return self._crawler_limit_rlt

    @crawler_limit_rlt.setter
    def crawler_limit_rlt(self, limit_tuple):
        self._crawler_limit_rlt = self.Crawler_limit(limit_tuple[0], limit_tuple[1], limit_tuple[2])

    @property
    def crawler_limit_his(self):
        return self._crawler_limit_his

    @crawler_limit_his.setter
    def crawler_limit_his(self, limit_tuple):
        self._crawler_limit_his = self.Crawler_limit(limit_tuple[0], limit_tuple[1], limit_tuple[2])

    @property
    def ngx_log(cls):
        return cls._ngx_log

    @ngx_log.setter
    def ngx_log(cls, filename):
        cls._ngx_log = filename

    @property
    def white_list(self):
        return self._white_list

    @white_list.setter
    def white_list(self, list):
        self.white_list = list

    @property
    def behav_list(self):
        return self._behav_list

    @behav_list.setter
    def behav_list(self, list):
        self._behav_list = list

    @property
    def blk_conf(self):
        return self._blk_conf

    @blk_conf.setter
    def blk_conf(self, filename):
        self._blk_conf = filename

    def ngx_logs(self, line_num=-1):
        """
        Getting nginx access.log by line_num and file
        ngx_log: default /var/log/nginx/access.log
        line_num: default -1, this parameter should minus 0
        """
        if line_num >= 0:
            print "line number should less than 0!"
            exit(1)
        else:
            try:
                lines = open(self.ngx_log, 'r').readlines()[line_num:]
            except IOError:
                print "Failed to get file: %s lines due to reason: %s" % (file, IOError)
            else:
                return lines

    def req_info(self, line=None):
        """
        Get request info by one line of access.log
        return a tuple(IP, Datatime, Requested dir/file, Response code, Bandwidth, Referrer, User agent)
        """
        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP address
               '\[(.+)\]\s'  # Datetime
               '"GET\s(.+)\s\w+/.+"\s'  # Requested dir/file
               '(\d+)\s'  # Response code
               '(\d+)\s'  # Bandwidth: $body_bytes_sent
               '"(.+)"\s'  # Referrer
               '"(.+)"'  # User agent
               )
        if line:
            req_info = re.findall(pat, line)[0]
            # TODO 1: req_info is like [()], get through to it
            if req_info:
                req_info = self.Req_info(req_info[0], req_info[1], req_info[2], req_info[3], req_info[4],
                                         req_info[5], req_info[6])
                return req_info
            return False

    def req_tm_gap(self, lines=None):
        """
        Get the time gap between first and last request info
        """
        try:
            start_line, end_line = lines[0], lines[-1]
            start_tm = time.strptime(self.req_info(start_line).Datatime, "%d/%b/%Y:%H:%M:%S +0000")
            end_tm = time.strptime(self.req_info(end_line).Datatime, "%d/%b/%Y:%H:%M:%S +0000")
            tm_gap = time.mktime(end_tm) - time.mktime(start_tm)
        except Exception as e:
            print "Failed get nginx time gap by line_num due to %s" % e
        else:
            return int(tm_gap)

    def crawler_behavs_re(self):
        """
        Define the crawler behaviour list pattern
        For example:
            1. we found someone crawler /airlines/*, so the behav_list should be ['airelines'];
            2. we found someone crawler /airlines/gh/*, so the behav_list should be ['airlines/gh']
        it is the keyworld of request url of nginx access.log
        """
        behavs_re = set()
        for behaviour in self.behav_list:
            behavs_re.add(r'(.*)?%s(.*)?' % behaviour)
        return list(behavs_re)

    @staticmethod
    def behav_match(req_info=None, behav_re=None):
        """
        Request info's Dir matches behaviours regex pattern
        """
        if behav_re and req_info is not None:
            if re.match(behav_re, req_info.Dir):
                return req_info.IP
            else:
                return None

    def line_judge(self, line=None):
        """
        one line in access.log whether matches crawler behavious
        """
        if line:
            try:
                behavs_re = self.crawler_behavs_re()
                reqinfo = self.req_info(line)
                for behav_re in behavs_re:
                    result = self.behav_match(reqinfo, behav_re)
                    return result if result else None
            except Exception as e:
                print "Failed to get IP due to %s" % e
        else:
            print "Not present line or behavious regex"
            return None

    def lines_judge(self, crawler_limit=None):
        """
        All lines in access.log whether matches crawler behavious
        """
        ip_dict = dict()
        crawler_ip_list = list()
        lines = self.ngx_logs(crawler_limit.Line_limit)
        tm_gap = self.req_tm_gap(lines)

        if tm_gap > crawler_limit.Tm_gap_limit:
            return None
        else:
            try:
                for line in lines:
                    result = self.line_judge(line)
                    if result:
                        if ip_dict.has_key(result):
                            ip_dict[self.line_judge(line)] += 1
                        else:
                            ip_dict[self.line_judge(line)] = 1
            except Exception as e:
                print "Failed to get crawler ip due to %s" % e
            else:
                for key, value in ip_dict.iteritems():
                    if value >= crawler_limit.Rate_limit:
                        crawler_ip_list.append(key)
                return crawler_ip_list

    def raw_crawler_ips_rlt(self):
        """
        Real time raw crawler ip list
        """
        raw_ip_list_rlt = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.crawler_limit_rlt)) as executor:
            rts = [ executor.submit(self.lines_judge, crawler_limit_rlt) for crawler_limit_rlt
                    in self.crawler_limit_rlt ]
            for rt in concurrent.futures.as_completed(rts):
                raw_ip_list_rlt += rt.result()
            raw_ip_list = list(set(raw_ip_list_rlt))
            return raw_ip_list

    def raw_crawler_ips_his(self):
        """
        Historical raw crawler ip list
        """
        raw_ip_list_his = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.crawler_limit_his)) as executor:
            rts = [executor.submit(self.lines_judge, crawler_limit_his) for crawler_limit_his
                   in self.crawler_limit_his]
            for rt in concurrent.futures.as_completed(rts):
                raw_ip_list_his += rt.result()
            raw_ip_list =list(set(raw_ip_list_his))
            return raw_ip_list

    def final_ip_list(self, ips=None):
        """
        Remove duplicate ip in blockips.conf and white list
        Add config to the file blackips.conf
        """
        ip_match = []

        with open(self.blk_conf, 'r+') as fd:
            for line in fd.readlines():
                ip_match += [ip for ip in ips if re.match(r"^deny\s%s;\n$" % ip, line)]
            blk_ips = [ip for ip in ips if ip not in ip_match + self.white_list]
            blk_ips_conf = ["deny %s;\n" % ip for ip in blk_ips]
            for ip in blk_ips_conf:
                fd.write(ip)
        return blk_ips




a = CrawlerIps()
a.ngx_log = './access.log-20170101'
l = a.raw_crawler_ips_rlt()
a.final_ip_list(l)