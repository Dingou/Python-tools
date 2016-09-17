"""
Fabric tasks for Saltstack Deployment
"""
import os
import sys
import json
from fabric.api import *


env.roledefs = {
    'master': ['localhost'],
}

OS_HOME_PATH_MAPPING = {
    'linux': 'home',
    'mac': 'Users',
    'jenkins': 'var/lib',
}

CONFIG = {
    'prod': {
        'branch': 'master',
        'key_file': 'salt',
        'git_remote': 'ylly',
    },
    'preprod': {
        'branch': 'develop',
        'key_file': 'salt',
        'git_remote': 'ylly',
    },
    'dev': {
        'branch': 'develop',
        'key_file': 'yl/devops/.vagrant/machines/default/virtualbox/private_key',
        'git_remote': 'ylly',
    },
}

REPORT = {
    'tasks': [],
    'commands': [],
    'successful': [],
    'failed': []
}

TRUE_VALUES = [True, "True", "true", "yes", 1]


# === Utility functions ===
def _get_os():
    """TODO: add docstring"""
    if os.uname()[0] == 'Darwin':
        return 'mac'
    return 'linux'


def _get_user():
    """TODO: add docstring"""
    user = os.environ.get('USER')
    return user


def _get_key_file(config, path_mapping=None):
    """TODO: add docstring"""
    home_path = 'home'
    path_mapping = path_mapping or OS_HOME_PATH_MAPPING
    if config['user'] in path_mapping:
        home_path = path_mapping[config['user']]
    elif config['os'] in path_mapping:
        home_path = path_mapping[config['os']]
    key_file_path = env.ssh_key_path % (
        home_path,
        config['user'],
        config['key_file']
    )
    return key_file_path


def _get_config():
    """
    Returns environment configuration
    """
    env.report = REPORT.copy()
    config = CONFIG[env.env]
    user = _get_user()
    config['os'] = _get_os()
    config['user'] = user
    config['remote_user'] = env.user or user
    config['home_dir'] = '/home/%(remote_user)s' % config
    return config


def _run(command, **kwargs):
    """TODO: add docstring"""
    res = sudo(command, **kwargs)
    env.report['commands'].append(res.command)
    if res.failed:
        env.report['failed'].append('%s >> %s' % (res.command, res))
    else:
        env.report['successful'].append(res.command)
    return res


def _report(name=''):
    """TODO: add docstring"""
    print '========================='
    print 'TASKS REPORT:', name
    print '-------------------------'
    print 'Total tasks:', env.report['tasks'].__len__()
    print 'Total commands:', env.report['commands'].__len__()
    print 'Successful:', env.report['successful'].__len__()
    print 'Failed:', env.report['failed'].__len__()
    if len(env.report['failed']) > 0:
        print '-------------------------'
        print 'ERRORS:'
        for command in env.report['failed']:
            print ' * ', command
    print '========================='
    # print json.dumps(env.report, indent=4)


# === Environments ===
def dev():
    """Sets the local dev config"""
    env.env = 'dev'
    env.user = 'vagrant'
    env.config = _get_config()
    env.salt = 'salt-call'
    env.run = _run
    env.port = '2222'
    env.ssh_key_path = '/%s/%s/%s'
    env.key_filename = _get_key_file(env.config)


def preprod():
    """Sets the preprod env config"""
    env.env = 'preprod'
    env.user = 'salt'
    env.config = _get_config()
    env.salt = 'salt'
    env.ssh_key_path = '/%s/%s/.ssh/%s'
    env.key_filename = _get_key_file(env.config)
    env.run = _run
    env.port = '2222'
    env.roledefs = {
        'master': ['bastion-pre.ylly.co'],
    }


def prod():
    """Sets the prod env config"""
    env.env = 'prod'
    env.user = 'salt'
    env.config = _get_config()
    env.salt = 'salt'
    env.ssh_key_path = '/%s/%s/.ssh/%s'
    env.key_filename = _get_key_file(env.config)
    env.run = _run
    env.port = '2222'
    env.roledefs = {
        'master': ['bastion.ylly.co'],
    }


@roles('master')
def salt(cmd=''):
    """Sets the minion id for saltstack deployment """
    if not cmd:
        cmd = "salt '*' test.ping"
    sudo(cmd)


@roles('master')
def minion(id="'*'"):
    """Sets the minion id for saltstack deployment """
    env.config['minion'] = id


@roles('master')
def command(module='test.ping', state='', test=False, loglevel='info'):
    """Sets the command for saltstack deployment """
    cmd = [env.salt]
    if env.salt == 'salt':
        minion = env.config.get('minion', "'bastion*'")
        cmd.append(minion)
    cmd.append(module)
    cmd.append(state)
    cmd.append('-l {}'.format(loglevel))
    if test in TRUE_VALUES:
        cmd.append('test=true')
    env.run(' '.join(cmd))
    _report('Saltstack deployment for {} environment'.format(env.env))


@roles('master')
def minion_keys():
    sudo('salt-key -L')