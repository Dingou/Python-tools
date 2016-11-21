# *.* coding: utf-8 *.*
import os
import re
import collections
import subprocess
import sys
import commands
import socket

def gzip_file_process(logfile=''):
    try:
        execute('gzip -d %s' % logfile)
        ungzip_file = re.sub("\.gz$", "", logfile)
        log_grep(ungzip_file)
        execute('gzip %s' % ungzip_file)
    except Exception as e:
        print "failed grep and filter .gzip log with keyworks due to %s" % e

def tar_file_process(logfile=''):
    try:
        execute('tar xvf %s' % logfile)
        untar_file = re.sub("\.tar$", "", logfile)
        log_grep(untar_file)
        execute('tar cvf %s %s' % (logfile,untar_file))
    except Exception as e:
        print "failed grep and filter .tar log with keyworks due to %s" % e

def zip_file_process(logfile=''):
    try:
        execute('unzip %s' % logfile)
        unzip_file = re.sub("\.zip$", "", logfile)
        log_grep(unzip_file)
        execute('zip %s' % unzip_file)
    except Exception as e:
        print "failed grep and filter .zip log with keyworks due to %s" % e

def tar_gzip_file_process(logfile=''):
    try:
        execute('tar xzvf %s' % logfile)
        untargzip_file = re.sub("\.tar\.gzip$", "", logfile)
        log_grep(untargzip_file)
        execute('tar czfv %s' % untargzip_file)
    except Exception as e:
        print "failed grep and filter .tar.gzip log with keyworks due to %s" % e

def normal_file_process(logfile=''):
    try:
        log_grep(logfile)
    except Exception as e:
        print "failed grep and filter .tar.gzip log with keyworks due to %s" % e

log_keyword_grep = 'grep "succeeded in" %s |awk -F\'s:\' \'{print $1}\''
log_remove_dupli = 'awk \'{ print $2}\' worker1.c1.ylly.co-celery-purify.log|awk -F\'[\' \'{ print $1}\''

pattern_end_gz = re.compile(r"(?<!(\.tar))\.gz$")
pattern_end_tar = re.compile(r"\.tar$")
pattern_end_zip = re.compile(r"\.zip$")
pattern_end_tar_gz = re.compile(r"\.tar\.gz$")

pattern_list = [pattern_end_gz, pattern_end_tar, pattern_end_zip, pattern_end_tar_gz]
pattern_dict = {pattern_end_gz: gzip_file_process, pattern_end_tar: tar_file_process,
                pattern_end_zip: zip_file_process, pattern_end_tar_gz: tar_gzip_file_process,
                'pattern_no_compress': normal_file_process}


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


def choose_pattern(logfile):
    i = 0
    while i < len(pattern_list):
        if pattern_list[i].search(logfile):
            return pattern_list[i]
        else:
            i += 1
            continue
    return 'pattern_no_compress'

def filter_output(output='',comp_condition='= 0'):
    purifylog = "%s-%s-purify.log" % (hostname,service)
    with open(purifylog,'a+') as f:
        for line in output.split('\n'):
            fields = line.strip().split()
            if eval('float(fields[-1]) %s' % comp_condition):
                f.write("%-20s\t%s\n" % (fields[-1], fields[4])) # you should rewrite this according to your scenario

def log_grep(logfile=''):
    (status, output) = commands.getstatusoutput(log_keyword_grep % (logfile))
    filter_output(output=output,comp_condition='> 600')


def log_filter(logfile=''):
    if logfile == '':
        print "No logfile provide!"
        sys.exit(0)
    else:
        try:
            pattern = choose_pattern(logfile)
            pattern_dict[pattern](logfile)
        except Exception as e:
            print "failed merging log due to %s" % e
        else:
            print "Done %s" % logfile

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