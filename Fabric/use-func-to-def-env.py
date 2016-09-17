#!/usr/bin/python

from fabric.api import *
import os



env.roledefs = {
    'hosts1': ['web1.hosts.com', 'web2.hosts.com'],
    'hosts2': ['web3.hosts.com', 'web4.hosts.com'],
}


SSH_KEY_PATH = '/%s/%s/.ssh/%s'

OS_HOME_PATH_MAPPING = {
    'linux': 'home',
    'mac': 'Users',
    'jenkins': 'var/lib',
}


CONFIG = {
    'hosts1': {
        'branch': 'master',
        'workspace': 'workspace',
        'project': 'web',
        'key_file': '1.pem',
        'git_remote': 'github',
    },
    'hosts2': {
        'branch': 'master',
        'workspace': 'workspace',
        'project': 'web',
        'key_file': '1.pem',
        'git_remote': 'github',
    }
}


def _get_user():
    """TODO: add docstring"""
    user = os.environ.get('USER')
    return user


def _get_settings():
    """
    set the settings based on the project
    """
    config = CONFIG[env.env]
    settings = {'hosts1': 'hosts1.settings.%(branch)s' % config, 'hosts2': 'erp.settings.%(branch)s' % config}
    for app_set in settings:
        config[app_set] = settings[app_set]

def _get_os():
    """TODO: add docstring"""
    if os.uname()[0] == 'Darwin':
        return 'mac'
    return 'linux'


def _get_config():
    """
    Returns environment configuration
    """
    config = CONFIG[env.env]
    user = _get_user()
    _get_settings()
    config['os'] = _get_os()
    config['user'] = user
    config['remote_user'] = env.user or user
    config['home_dir'] = '/home/%(remote_user)s' % config
    config['venv'] = '%(home_dir)s/virtualenv/bin' % config
    config['workspace_dir'] = '%(home_dir)s/%(workspace)s' % config
    config['project_dir'] = '%(workspace_dir)s/%(project)s' % config
    return config


# === Environments ===
def dev():
    """TODO: add docstring"""
    #    from cruise2.settings import dev
    #    env.settings = dev
    env.env = 'dev'
    env.config = _get_config()
    env.run = local


def preprod():
    """Sets the preprod config"""
    #    from cruise2.settings import prod
    #    env.settings = prod
    env.env = 'hosts1'
    env.user = 'ubuntu'
    env.config = _get_config()
    env.run = run
    env.roledefs = {
        'hosts1': ['web1.hosts.com', 'web2.hosts.com'],

    }
