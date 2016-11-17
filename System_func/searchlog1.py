# *.* coding: utf-8 *.*
import os
import re
import collections
import subprocess
import sys
import commands

merge_file = 'total.log'
log_merge_filter = 'grep "succeeded in" %s |awk -F\'s:\' \'{print $1}\' >> %s'
log_purify = 'awk \'{if($NF>600) print $NF,$5}\' total.log > purify.log'

pattern_gz = re.compile(r"\.gz$")
pattern_log = re.compile(r"^celery.log(-\d+\.gz)?$")

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


def log_merge(logfile=''):
    if logfile == '':
        print "No logfile provide!"
        sys.exit(0)
    else:
        try:
            if pattern_gz.search(logfile):
                execute('gzip -d %s' % logfile)
                ungzip_file = re.sub("\.\w+$","",logfile)
                (status, output) = commands.getstatusoutput(log_merge_filter % (ungzip_file, merge_file))
                execute('gzip %s' % ungzip_file)
            else:
                (status, output) = commands.getstatusoutput(log_merge_filter % (logfile, merge_file))
        except Exception as e:
            print "failed merging log due to %s" % e
        else:
            print "Done %s" % logfile


def main(log_purify='awk \'{if($NF>600) print $NF,$5}\' total.log > purify.log'):
    map(log_merge, os.listdir(os.getcwd()))
    (status, output) = commands.getstatusoutput(log_purify)

if __name__ == "__main__":
    """
    All file to totalfile
    then purify totalfile
    """
    main()