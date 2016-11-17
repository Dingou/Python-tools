# *.* coding: utf-8 *.*
import os
import re
import collections
import subprocess
import sys
import commands
import socket

log_keyword_grep = 'grep "succeeded in" %s |awk -F\'s:\' \'{print $1}\''
log_remove_dupli = 'awk \'{ print $2}\' worker1.c1.ylly.co-celery-purify.log|awk -F\'[\' \'{ print $1}\''

pattern_end_gz = re.compile(r"\.gz$")
pattern_end_tar = re.compile(r"\.tar$")
pattern_end_zip = re.compile(r"\.zip$")
pattern_end_tar_zip = re.compile(r"\.tar\.zip$")
pattern_end_tar_gzip = re.compile(r"\.tar\.gzip$")

pattern_celery_log = re.compile(r"^celery.log(-\d+\.gz)?$")

hostname = socket.gethostname()
service = 'service'

ExecutionResult = collections.namedtuple(
    'ExecutionResult',
    'status, stdout, stderr'
)

def execute(cmd, **kwargs):
    splitted_cmd = cmd.split()
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    try:
        process = subprocess.Popen(splitted_cmd, **kwargs)
        stdout, stderr = process.communicate()
        status = process.poll()
        return ExecutionResult(status, stdout, stderr)
    except OSError as e:
        print("Command exec error: '%s' %s" % (cmd, e))
        return ExecutionResult(1, '', '')

def common_process(logfile=''):
    (status, output) = commands.getstatusoutput(log_keyword_grep % (logfile))
    filter_output(output)

def gzip_file_process(logfile=''):
    try:
        execute('gzip -d %s' % logfile)
        ungzip_file = re.sub("\.gzip$", "", logfile)
        common_process(ungzip_file)
        execute('gzip %s' % ungzip_file)
    except Exception as e:
        print "failed grep and filter .gzip log with keyworks due to %s" % e

def tar_file_process(logfile=''):
    try:
        execute('tar xvf %s' % logfile)
        untar_file = re.sub("\.tar$", "", logfile)
        common_process(untar_file)
        execute('tar cvf %s %s' % (logfile,untar_file))
    except Exception as e:
        print "failed grep and filter .tar log with keyworks due to %s" % e

def zip_file_process(logfile=''):
    try:
        execute('unzip %s' % logfile)
        unzip_file = re.sub("\.zip$", "", logfile)
        common_process(unzip_file)
        execute('zip %s' % unzip_file)
    except Exception as e:
        print "failed grep and filter .zip log with keyworks due to %s" % e

def tar_gzip_file_process(logfile=''):
    try:
        execute('tar xzvf %s' % logfile)
        untargzip_file = re.sub("\.tar\.gzip$", "", logfile)
        common_process(untargzip_file)
        execute('tar czfv %s' % untargzip_file)
    except Exception as e:
        print "failed grep and filter .tar.gzip log with keyworks due to %s" % e


def log_filter(logfile=''):
    if logfile == '':
        print "No logfile provide!"
        sys.exit(0)
    else:
        try:
            if pattern_end_gz.search(logfile):
                gzip_file_process(logfile)
            elif

        except Exception as e:
            print "failed merging log due to %s" % e
        else:
            print "Done %s" % logfile

def filter_output(output=''):
    purifylog = "%s-%s-purify.log" % (hostname,service)
    with open(purifylog,'a+') as f:
        for line in output.split('\n'):
            fields = line.strip().split()
            if float(fields[-1]) >= 600:
                f.write("%-20s\t%s\n" % (fields[-1], fields[4]))

def remove_dup():
    (status, output) = commands.getstatusoutput(log_remove_dupli)
    mylist = list(set(output.split('\n')))
    myliststr  = ' '.join(mylist)
    mylist_file = "%s-celery-tasks" % hostname
    with open(mylist_file, 'a+') as f:
        f.write(myliststr)


def main():
    file_list = []
    for file in os.listdir(os.getcwd()):
        if pattern_celery_log.search(file):
            file_list.append(file)
    map(log_filter, file_list)

if __name__ == "__main__":
    """All file to totalfile
    then purify totalfile
    """
    main()