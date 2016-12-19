import commands
import time
import concurrent.futures
import re
import subprocess
import shlex

raw_cmd = "tail -n %s %s|%s"
ngx_log = '/var/log/nginx/access.log'
#black_conf_file = '/etc/nginx/conf.d/blockips.conf'
black_conf_file = '/root/crawlerip.txt'
grep_head_partten = 'head -n 1'
filter_ELB_HEAD_pattern = 'grep -E -v \"ELB-HealthChecker/1.0|HEAD\"'
filter_cruises_req_pattern = 'grep -E "GET /cruises/[0-9]*'
sort_by_ip_visit_num_pattern = 'awk \'{IP[$1]++}END{ for(Num in IP) print Num, IP[Num]}\'|sort -nr -k 2'
filter_ip_by_frequency_pattern = 'awk  \'{if($2>=limit) print $1}\' limit=%d'
extract_ip_in_file_cmd = 'cat %s|awk \'{ print $2 }\'' % black_conf_file
#whitelist_pattern = ['^54.223.+', '^172.+']
whitelist_pattern = ['192.168.1.1']
nginx_reload_cmd = "nginx -s reload"

def ngx_time_interval(line_num):
    try:
        ngx_headlog_cmd = raw_cmd % (line_num, ngx_log, grep_head_partten)
        (status, stdout) = commands.getstatusoutput(ngx_head_log_cmd)
        nginx_time = stdout[(stdout.index('[') + 1):(stdout.index(']') - 6)]
        t = time.strptime(nginx_time, "%d/%b/%Y:%H:%M:%S")
        starttime = time.mktime(t)
        endtime = time.time()
        time_interval = endtime - starttime
        return int(time_interval)
    except Exception as e:
        print "Failed get nginx time interval by linenumber due to %s" % e

def ngx_cruises_crawler_suspect_ip(line_frequency_limit_tuple):
    try:
        line_num = line_frequency_limit_tuple[0]
        frequency_limit = line_frequency_limit_tuple[1]
        filter_ip_by_frequency_limit_pattern = filter_ip_by_frequency_pattern % frequency_limit
        filter_pattern = "%s|%s|%s" % (filter_ELB_HEAD_pattern, sort_by_ip_visit_num_pattern, filter_ip_by_frequency_limit_pattern)
        ngx_cruises_visit_count_by_ip_cmd = raw_cmd % (line_num, ngx_log, filter_pattern)
        (status, IPS) = commands.getstatusoutput(ngx_cruises_visit_count_by_ip_cmd)
        if status == 0:
            return IPS.split('\n')
    except Exception as e:
        print "Failed get nginx cruises page crawler ip due to %s" % e

def ip_in_whiltelist(ip):
    result = 0
    try:
        for ip_pattern in whitelist_pattern:
            prog = re.compile(ip_pattern)
            if prog.match(ip):
                result += 1
    except Exception as e:
        print "Failed filter ip due to %s" % e
    else:
        return None if result != 0 else ip


class Anti_Crawler(object):
    whitelist_pattern = whitelist_pattern
    line_nums = [500, 1000, 5000, 10000]
    frequency_limits = [150, 300, 1000, 3000]
    time_interval_limits = [1800, 3600, 18000, 36000]
    def __init__(self):
        self.ngx_time_interval_func = ngx_time_interval
        self.ngx_cruises_crawler_suspect_ip_func = ngx_cruises_crawler_suspect_ip
        self.ip_in_whiltelist_func = ip_in_whiltelist
    def line_frequency_limit_dict(self):
        try:
            return dict(zip(self.line_nums, self.frequency_limits)).items()
        except Exception as e:
            print "Failed return line_frequency_limit_dict due to %s" % e
    def ngx_time_interval_list_conc(self):
        time_interval_list = []
        max_worker = len(self.line_nums)
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_worker) as executor:
                for time_interval in executor.map(self.ngx_time_interval_func, self.line_nums):
                    time_interval_list.append(time_interval)
        except Exception as e:
            print "Failed return time_interval_list due to %s" % e
        else:
            return time_interval_list
    def ngx_cruises_crawler_suspect_ip_conc(self):
        line_frequency_limit_dict = self.line_frequency_limit_dict()
        iplist = []
        max_worker = len(self.line_nums)
        try:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_worker) as executor:
                for IPS in executor.map(self.ngx_cruises_crawler_suspect_ip_func, line_frequency_limit_dict):
                    iplist += IPS
        except Exception as e:
            print "Failed return ip_list due to %s" % e
        else:
            return iter(list(set(iplist)))
    def new_crawler_iplist(self):
        new_crawler_iplist =  filter(self.ip_in_whiltelist_func, [ x for x in self.ngx_cruises_crawler_suspect_ip_conc() ])
        (status , raw_exist_crawler_iplist) = commands.getstatusoutput(extract_ip_in_file_cmd)
        lastone = raw_exist_crawler_iplist.split(';\n')[-1][:-1]
        exist_crawler_iplist = raw_exist_crawler_iplist.split(';\n')[:-1]
        exist_crawler_iplist.append(lastone)
        new_crawler_iplist = [ x for x in new_crawler_iplist if x not in exist_crawler_iplist ]
        return new_crawler_iplist
    def write_to_config(self):
        new_crawler_iplist = self.new_crawler_iplist()
        print new_crawler_iplist
        if len(new_crawler_iplist) != 0:
            try:
                with open(black_conf_file, 'a+') as f:
                    for ip in new_crawler_iplist:
                        f.write("deny %s;\n" % ip)
            except Exception as e:
                print "Failed write to config  due to %s" % e
            else:
                args = shlex.split(nginx_reload_cmd)
                result = subprocess.Popen(args)
                return result

a = Anti_Crawler()
t = a.new_crawler_iplist()