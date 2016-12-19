"""
Fabric tasks for Saltstack Deployment
"""
import os
import sys
import json
from fabric.api import *
from fabric.contrib.files import sed, contains


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
    config['salt_file_dir'] = '/srv/devops/'
    config['salt_pillar_dir'] = '/srv/pillar'
    config['salt_config_file'] = '/etc/salt/master'
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
    env.port = '4916'
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
    env.port = '4916'
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
    env.port = '4916'
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
def command(module='test.ping', state='', test=False, loglevel='info', out_diff=False):
    """Sets the command for saltstack deployment """
    cmd = [env.salt]
    if env.salt == 'salt':
        minion = env.config.get('minion', "'bastion*'")
        cmd.append(minion)
    cmd.append(module)
    cmd.append(state)
    cmd.append('-l {}'.format(loglevel))
    if out_diff in TRUE_VALUES:
        cmd.append('--output-diff')
    if test in TRUE_VALUES:
        cmd.append('test=true')
    env.run(' '.join(cmd))
    _report('Saltstack deployment for {} environment'.format(env.env))


@roles('master')
def minion_keys():
    sudo('salt-key -L')


@roles('master')
def refresh_cache():
    minion = env.config.get('minion', "'*'")
    sudo('salt {0} saltutil.refresh_pillar'.format(minion))
    sudo('salt {0} saltutil.refresh_modules'.format(minion))
    sudo('salt {0} state.clear_cache'.format(minion))


@roles('master')
def pull():
    for salt_path in [env.config['salt_file_dir'], env.config['salt_pillar_dir']]:
        with cd(salt_path):
            sudo('git fetch origin {branch} && git checkout {branch}'.format(**env.config))
            sudo('git pull origin {branch}'.format(**env.config))
    update_master_configure()


@roles('master')
def branch(name=None):
    if name:
        env.config['branch'] = name


@roles('master')
def update_master_configure():
    pattern = 'gitfs_base: '+env.config['branch']
    if not contains(env.config['salt_config_file'], pattern):
        sed(env.config['salt_config_file'],
            '^gitfs_base:.*$',    # <before> pattern for replacement
            'gitfs_base: '+env.config['branch'],   # <after> replacement to
            use_sudo=True,       # with sudo
            shell=True)
        restart_master()


@roles('master')
def restart_master():
    sudo('rm -rf /var/cache/salt', settings(warn_only=True))
    for srv in ['salt-master', 'salt-minion', 'salt-api']:
        sudo('service {} restart'.format(srv), settings(warn_only=True))