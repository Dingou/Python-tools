import commands
import time
import concurrent.futures

line_nums = [500, 1000, 5000, 10000, 50000, 100000]
file_name = '/var/log/nginx/access.log'
raw_cmd = "tail -n %s %s|grep -E -v \"ELB-HealthChecker/1.0|HEAD\"|head -n 1"

def time_interval(line_num):
    cmd = raw_cmd % (line_num, file_name)
    (status, stdout) = commands.getstatusoutput(cmd)
    nginx_time = stdout[(stdout.index('[')+1):(stdout.index(']')-6)]
    t = time.strptime(nginx_time, "%d/%b/%Y:%H:%M:%S")
    starttime = time.mktime(t)
    endtime = time.time()
    time_inter = endtime - starttime
    return time_inter

def conc():
    time_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        for time_inter in executor.map(time_interval, line_nums):
            time_list.append(int(time_inter))
