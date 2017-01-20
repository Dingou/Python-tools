# -*- coding: utf-8 -*-
from collections import namedtuple
import time
import concurrent.futures
import re

# Todo: 1. add service reload (done)
# Todo: 2. add __main__ function
# Todo: 3. optimize;
# Todo: 4. distribute get crawler ip in access.log(Or we can use ELK instead)
# Todo: 5. juge crawler by USER AGENTs


class CrawlerIps(object):
    """
    To get Crawler Ips by crawler behaviours which you could find in nginx access.log
    use __slots__ to limit property setter
    """

    __slots__ = ('crawler_limit_real_tm', 'crawler_limit_history', 'ngx_log', 'white_list', 'behav_list', 'blk_conf',
                 '_crawler_limit_real_tm', '_crawler_limit_history', '_ngx_log', '_white_list', '_behav_list',
                 '_blk_conf', '_max_wks', 'mks_wks', '_user_agents', 'user_agents')



    # Req_info:
    # IP: request ip, like 192.168.1.1
    # Datatime: request time, like "%d/%b/%Y:%H:%M:%S +0000"
    # Dir: request path, like '/'
    # Status: response code, like 200, 301, 302, 403
    # BandWidth: $body_bytes_sent
    # Referrer: Referrer
    # UserAgent: User Agent/Browser
    Request_info = namedtuple('Request_info', ['IP', 'Datatime', 'Dir', 'Status', 'BandWidth', 'Referrer', 'UserAgent'])

    def __init__(self):
        """
        _crawler_limit_real_tm: real time Crawler_limit list, you could use this to detect ip on real time
        _crawler_limit_his: historic Crawler_limit list, you could detect historic crawler ip
        _ngx_log: nginx access log
        _white_list: white list ips
        _behav_list: crawler behavious, e.g: spider always crawler '/airplanes/135181983123/',
                     so we add airplanes to list
        _blk_conf: nginx black list config
        _max_wks: max works for concurrent by set
        """
        self._crawler_limit_real_tm = [self.Crawler_limit(-500, 150, 1800), self.Crawler_limit(-1000, 300, 3600),
                                   self.Crawler_limit(-3000, 900, 10400)]
        self._crawler_limit_history = [self.Crawler_limit(-5000, 1000, 18000)]
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
    def crawler_limit_real_tm(self):
        return self._crawler_limit_real_tm

    @crawler_limit_real_tm.setter
    def crawler_limit_real_tm(self, limit_tuple):
        self._crawler_limit_real_tm = self.Crawler_limit(limit_tuple[0], limit_tuple[1], limit_tuple[2])

    @property
    def crawler_limit_history(self):
        return self._crawler_limit_history

    @crawler_limit_history.setter
    def crawler_limit_history(self, limit_tuple):
        self._crawler_limit_history = self.Crawler_limit(limit_tuple[0], limit_tuple[1], limit_tuple[2])

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
                logs = open(self.ngx_log, 'r').readlines()[line_num:]
            except IOError:
                print "Failed to get file: %s lines due to reason: %s" % (file, IOError)
            else:
                return logs

    def request_info(self, line=None):
        """
        Get request info by one line of access.log
        return a tuple(IP, Datatime, Requested dir/file, Response code, Bandwidth, Referrer, User agent)
        """
        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'
               '\[(.+)\]\s'
               '"GET\s(.+)\s\w+/.+"\s'
               '(\d+)\s'
               '(\d+)\s'
               '"(.+)"\s'
               '"(.+)"'
               )
        if line:
            request_info = re.findall(pat, line)[0]
            # TODO 1: request_info is like [()], get through to it
            if request_info:
                request_info = self.Request_info(request_info[0], request_info[1], request_info[2], request_info[3],
                                             request_info[4], request_info[5], request_info[6])
                return request_info
            return False

    def request_tm_gap(self, lines=None, start=0, end=-1):
        """
        Get the time gap between first and last request info
        """
        start_log, end_log = lines[start], lines[end]
        try:
            start_tm = time.strptime(self.request_info(start_log).Datatime, "%d/%b/%Y:%H:%M:%S +0000")
            end_tm = time.strptime(self.request_info(end_log).Datatime, "%d/%b/%Y:%H:%M:%S +0000")
            tm_gap = time.mktime(end_tm) - time.mktime(start_tm)
        except Exception as e:
            print "Failed get nginx time gap by logs due to %s" % e
        else:
            return int(tm_gap)

    def crawler_re(self):
        """
        Define the crawler list pattern by keywords in nginx
        For example:
            1. some crawler request '/airlines/*' time by time, so the crawler_pattern should be ['airelines'];
            2. some crawler request '/airlines/gh/*' time by time, so the crawler_pattern should be ['airlines/gh'];
            3. some crawler request '/airlines/*' time by time with one kind of User Agent,so

        """
        filter_re = set()
        for behaviour in self.behav_list:
            filter_re.add(r'(.*)?%s(.*)?' % behaviour)
        return list(filter_re)

    @staticmethod
    def filter_match(request_info=None, filter_re=None, filter_option=0):
        """
        Request info's Dir matches behaviours regex pattern
        :
        """
        if filter_re and request_info is not None:
            if re.match(filter_re, request_info.Dir) or re.match(filter_re, request_info.Dir):
                return request_info.IP
            else:
                return None

    def log_search(self, line=None):
        """
        one line in access.log whether matches crawler behavious
        """
        if line:
            try:
                filter_re = self.crawler_re()
                reqinfo = self.request_info(line)
                for behav_re in filter_re:
                    result = self.filter_match(reqinfo, behav_re)
                    return result if result else None
            except Exception as e:
                print "Failed to get IP due to %s" % e
        else:
            print "Not present line or behavious regex"
            return None

    def logs_search(self, crawler_limit=None):
        """
        All lines in access.log whether matches crawler behavious
        """
        ip_dict = dict()
        crawler_ip_list = list()
        lines = self.ngx_logs(crawler_limit.Line_limit)
        tm_gap = self.request_tm_gap(lines)

        if tm_gap > crawler_limit.Tm_gap_limit:
            return None
        else:
            try:
                for line in lines:
                    result = self.log_search(line)
                    if result:
                        if ip_dict.has_key(result):
                            ip_dict[self.log_search(line)] += 1
                        else:
                            ip_dict[self.log_search(line)] = 1
            except Exception as e:
                print "Failed to get crawler ip due to %s" % e
            else:
                for key, value in ip_dict.iteritems():
                    if value >= crawler_limit.Rate_limit:
                        crawler_ip_list.append(key)
                return crawler_ip_list

    def raw_crawler_ips_real_tm(self):
        """
        Real time raw crawler ip list
        """
        raw_ip_list_real_tm = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.crawler_limit_real_tm)) as executor:
            rts = [ executor.submit(self.logs_search, crawler_limit_real_tm) for crawler_limit_real_tm
                    in self.crawler_limit_real_tm ]
            for rt in concurrent.futures.as_completed(rts):
                raw_ip_list_real_tm += rt.result()
            raw_ip_list = list(set(raw_ip_list_real_tm))
            return raw_ip_list

    def raw_crawler_ips_history(self):
        """
        Historical raw crawler ip list
        """
        raw_ip_list_history = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.crawler_limit_history)) as executor:
            rts = [executor.submit(self.logs_search, crawler_limit_history) for crawler_limit_history
                   in self.crawler_limit_history]
            for rt in concurrent.futures.as_completed(rts):
                raw_ip_list_history += rt.result()
            raw_ip_list =list(set(raw_ip_list_history))
            return raw_ip_list

    def raw_crawler_by_user_agent(self):
        """
        filter raw ips by UserAgent
        """
        raw_ip_list_user_agent = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.user_agents)) as executor:
            rts = [executor.submit(self.logs_search, crawler_user_agent) for crawler_user_agent
                   in self.user_agents]
            for rt in concurrent.futures.as_completed(rts):
                raw_ip_list_user_agent += rt.result()
            raw_ip_list_user_agent = list(set(raw_ip_list_user_agent))
            return raw_ip_list_user_agent

    def final_ip_list(self, ips=None):
        """
        Remove duplicate ip in blockips.conf and white list
        Add config to the file blackips.conf
        """
        ip_already_blk = []

        with open(self.blk_conf, 'r+') as fd:
            for line in fd.readlines():
                ip_already_blk += [ip for ip in ips if re.match(r"^deny\s%s;\n$" % ip, line)]
            blk_ips = [ip for ip in ips if ip not in ip_already_blk + self.white_list]
            blk_ips_conf = ["deny %s;\n" % ip for ip in blk_ips]
            for new_ip_blk_conf in blk_ips_conf:
                fd.write(new_ip_blk_conf)
        return blk_ips

a = CrawlerIps()
a.ngx_log = './access.log-20170101'
l = a.raw_crawler_ips_real_tm()
a.final_ip_list(l)