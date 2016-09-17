"""
Dump Database Utils
"""

import os
import logging

from commandr import command, Run
from fabric.api import env, run, local, cd, put
from fabric.contrib.files import exists

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def _get_config():
    """
    Returns environment configuration
    :rtype : dict
    """
    section = os.getcwd().split('/')[2]
    if section == 'sanitized':
        config = _load_yaml('youlun')
    elif section == 'dump':
        config = _load_yaml('dump')
    else:
        logging.error("No section found in yaml file")

    config.update(config['mysqldump'])
    config.update(config['esdump'])
    config.update(config['dump_mirrors'])
    config['json_suffix'] = 'json'
    config['archive_suffix'] = 'xz'
    config['index_json_file'] = '%(es_prod_index)s.%(json_suffix)s' % config
    config['sql_dump'] = 'cruise.sql'
    config['sanitized_sql_dump'] = 'sanitized-cruise.sql'
    config['new_dbdump_file'] = '%(dbdump_file)s.new' % config
    config['new_esdump_file'] = '%(esdump_file)s.new' % config
    config['dbdump_dir'] = '%(home_dir)s/%(db_workspace)s' % config
    config['esdump_dir'] = '%(home_dir)s/%(es_workspace)s' % config
    config['local_dbdump'] = '%(dbdump_dir)s/%(dbdump_file)s' % config
    config['local_esdump'] = '%(esdump_dir)s/%(esdump_file)s' % config
    env.user = config['user'] or env.user
    env.key_filename = os.path.join(os.environ.get('HOME'), '.ssh/%(ssh_key)s' % config)
    env.port = config['ssh_port']
    env.connection_attempts = 5
    env.run = run
    env.put = put
    return config


# === Define Environments ===
def local():
    """Define the local environment with the environment variables
    """
    env.env = 'local'
    env.config = _get_config()
    env.run = local
    env.host_string = 'localhost'


def prod():
    """Define the production environment with the environment variables
    """
    env.env = 'bastion'
    env.config = _get_config()
    env.host_string = '%s.ylly.co' % env.env


def preprod():
    """Define the pre-prod environment with the environment variables
    """
    env.env = 'bastion-pre'
    env.config = _get_config()
    env.host_string = '%s.ylly.co' % env.env


def _load_yaml(section='mysqldump'):
    """
    load the database information from yaml config,
    :param section: load the specified section in the yaml file.
    :type section: str
    :return dict
    """
    try:
        from YamJam import yamjam
        dbinfo = yamjam()[section]
    except (ImportError, KeyError):
        dbinfo = {}
    return dbinfo


@command('db_export')
def db_export(dump_dst=None, from_db='dumpreplica'):
    """
    export the dump file from database.
    :param dump_dst: the destination directory for create dump file.
    :type dump_dst: str
    :param from_db: export which database.
    :type from_db: str
    """
    dbinfo = _load_yaml(from_db)
    config = _get_config()
    dbinfo['db_conf'] = config['db_conf'] = os.path.join(config['dbdump_dir'], '.db.%s.conf' % from_db)
    dbinfo['new_dbdump_file'] = config['new_dbdump_file'] = '%s.%s' % (config['dbdump_file'], from_db)

    dump_dst = dump_dst if dump_dst is not None else from_db
    workspace = os.path.join(config['dbdump_dir'], dump_dst)

    if not exists(workspace):
        env.run('mkdir -p %s' % workspace)

    with cd(workspace):
        logging.info('switched the directory to %s to create dump file ' % workspace)
        logging.info("Starting exporting datbase %(host)s to dump file %(new_dbdump_file)s." % dbinfo)
        try:
            env.run('mysqldump --defaults-extra-file=%(db_conf)s \
                    -h %(host)s --quick %(name)s | pv | xz -0 \
                    > %(new_dbdump_file)s' % dbinfo)
            env.run('rm -f %(dbdump_file)s' % config)
            env.run('mv %(new_dbdump_file)s %(dbdump_file)s' % config)
        except Exception, e:
            logging.error('Create database dump file failure for %s', str(e))


@command('db_import')
def db_import(from_db='dumpreplica', to_db='preprod'):
    """
    Import the dump file to specified database.
    :param from_db: from which database's dump file to import
    :type from_db: str
    :param to_db: import to which database.
    :type to_db: str
    """

    dbinfo = _load_yaml(to_db)
    config = _get_config()
    dbinfo['db_conf'] = config['db_conf'] = os.path.join(config['dbdump_dir'], '.db.%s.conf' % to_db)
    if to_db == "sanitized":
        dbinfo['sql_dump'] = config['sanitized_sql_dump']
    else:
        dbinfo['sql_dump'] = config['sql_dump']

    workspace = os.path.join(config['dbdump_dir'], to_db)

    with cd(workspace):
        logging.info("Preparing to import the database %(host)s from " % dbinfo + from_db)
        if exists(config['dbdump_file']):
            try:
                run('rm -f %(sql_dump)s' % dbinfo)
                run('unxz -f %(dbdump_file)s' % config)
                logging.info("Start to importing the sql dump to the database instance for the %s." % to_db)
                run('{ pv %(sql_dump)s ; } | mysql --defaults-extra-file=%(db_conf)s -A -h %(host)s %(name)s'
                    % dbinfo)
                logging.info("Database %(host)s Update finished!" % dbinfo)
            except Exception, e:
                logging.error('Update pre-prod database failure because %s', str(e))


@command('db_cltables')
def db_cltables(to_db='preprod'):
    """
    Delete database tables before import
    """
    dbinfo = _load_yaml(to_db)
    config = _get_config()
    dbinfo['db_conf'] = config['db_conf'] = os.path.join(config['dbdump_dir'], '.db.%s.conf' % to_db)

    logging.info('Begin to clear the tables(Keep database)')

    try:
        env.run('mysql --defaults-extra-file=%(db_conf)s -A -h %(host)s -D%(name)s -BNe "show tables" | \
                awk \'{ print "set foreign_key_checks=0; drop table `" $1"`;"}\' | \
                mysql --defaults-extra-file=%(db_conf)s -A -h %(host)s -D %(name)s' % dbinfo)

        logging.info("Database %(host)s tables cleared!" % dbinfo)
    except Exception, e:
        logging.error('Clear pre-prod tables failure because %s'. str(e))



def push_dump(db=False, es=False):
    """push the dump file to the other host(jenkins master for now).
    :param db: if push the database dump file.
    :type db: bool
    :param es: if push the es dump file.
    :type es: bool
    """
    config = _get_config()

    mirrors = config['dump_mirrors']
    for mirror, mirrorinfo in mirrors.iteritems():
        env.user = mirrorinfo['dump_user']
        env.port = 22
        env.host_string = mirrorinfo['dump_domain']
        env.dump_path = mirrorinfo['dump_path']
        try:
            with cd(env.dump_path):
                if db:
                    env.run('rm -f %(new_dbdump_file)s' % config)
                    env.put('%(local_dbdump)s' % config, '%(new_dbdump_file)s' % config)
                    env.run('rm -f %(dbdump_file)s' % config)
                    env.run('mv %(new_dbdump_file)s %(dbdump_file)s' % config)
                if es:
                    env.run('rm -f %(new_esdump_file)s' % config)
                    env.put('%(local_esdump)s' % config, '%(new_esdump_file)s' % config)
                    env.run('rm -f %(esdump_file)s' % config)
                    env.run('mv %(new_esdump_file)s %(esdump_file)s' % config)
        except Exception, e:
            logging.error('Failed to push dump file to remote host %s. Reason: %s' % (mirror['dump_domain'], str(e)))


def index_dump(index_types=['mapping', 'data']):
    """
    export the specified index from the ES.
    :param index_types: a list for the export index type
    :type index_types: list

    # https://github.com/taskrabbit/elasticsearch-dump
    """

    esinfo = _get_config()
    push_json_archive = []
    workspace = esinfo['esdump_dir']
    with cd(workspace):
        logging.info("Preparing to dump the index from production.")
        for t in index_types:
            esinfo.update({'type': t})
            esinfo.update({'file_archive': esinfo['es_prod_index'] + '_' + t + '.json'})
            try:
                env.run('rm -f %(file_archive)s' % esinfo)
                env.run('elasticdump \
                             --input=http://%(es_prod_addr)s:9200/%(es_prod_index)s \
                             --type=%(type)s \
                             --output=%(file_archive)s' % esinfo)
                push_json_archive.append(esinfo['file_archive'])
            except Exception, e:
                logging.error('dump the indies failure from production, caused of %s', str(e))
        try:
            env.run('tar c ' + ' '.join(push_json_archive) + '| xz -0 > %(new_esdump_file)s' % esinfo)
            env.run('rm -f %(esdump_file)s' % esinfo)
            env.run('mv %(new_esdump_file)s %(esdump_file)s' % esinfo)
            logging.info("dump the index successful!")
        except Exception, e:
            logging.error('archive the dump the index failure for %s', str(e))


@command('sync_preprod_indies')
def index_sync():
    """
    sync the all of indies from production to pre-prod.
    # https://github.com/taskrabbit/elasticsearch-dump
    """

    esinfo = _get_config()
    workspace = os.path.join(esinfo['esdump_dir'], 'preprod')

    if not exists(workspace):
        env.run('mkdir -p %s' % workspace)

    with cd(workspace):
        logging.info("Preparing to sync the index from production to pre-prod.")
        try:
            env.run('rm -f %(index_json_file)s' % esinfo)
            env.run('elasticdump \
                         --all=true \
                         --input=http://%(es_prod_addr)s:9200/ \
                         --output=%(index_json_file)s' % esinfo)
            if exists(esinfo['index_json_file']):
                env.run('elasticdump \
                         --bulk=true \
                         --input=%(index_json_file)s \
                         --output=http://%(es_preprod_addr)s:9200/'
                          % esinfo)
                logging.info("sync the index from production to pre-prod successful!")
            else:
                logging.error("Didn't locate the index dump file during sync the indies to pre-prod.")
        except Exception, e:
            logging.error('sync the indies failure from production to pre-prod, caused of %s', str(e))

@command("update_database")
def update_database(dump_dst=None,from_db=None,to_db=None):
    """
    update database function,this is a refactor for updata_* alias
    :param dump_dst: dump destion database
    :param from_db: from where to dump
    :param to_db: clear or import to database name
    """
    db_export(dump_dst,from_db)
    db_cltables(to_db)
    db_import(from_db,to_db)


@command('update_preprod')
def update_preprod():
    """
    update the database for the preprod
    :param db:
    """
    db_export(dump_dst='preprod', from_db='dumpreplica')
    db_cltables('preprod')
    db_import('dumpreplica', 'preprod')


@command('update_standby')
def update_standby():
    """update the database for instance of standby
    """
    db_export(dump_dst='standby', from_db='dumpreplica')
    db_import('dumpreplica', 'standby')


@command('update_download')
def update_download(db=False, es=False):
    """
    create and push the dump file to the other host for serving download during the update_db action.
    :param db: if push the db dump file.
    :type db: bool
    :param es: if push the es dump file.
    :type es: bool
    :param dump_dst: set dump_dst database name.
    :type dump_dst: string
    """
    if db:
        db_export(dump_dst='', from_db='dumpreplica')
    if es:
        index_dump()
    push_dump(db, es)


@command('update_sanitized')
def update_sanitized():
    """
    Step 1.update the bastion-pre(database cruise-sanitized)from cruise-dump databases
    Step 2.Sanitize cruise-sanitized
    Step 3.export sanitized cruise-sanitized and upload to mirrors of (beijing|tokyo)
    """
    config = _get_config()
    logging.info("Begin to update sanitized_database...")
    #Step 1
    try:
        db_export(dump_dst='sanitized', from_db='dumpreplica')
        db_cltables('sanitized')
        db_import('dumpreplica', 'sanitized')
    except Exception, e:
        logging.error('Update sanitized_database failure because %s', str(e))

    youlun_workspace = os.path.join(config['home_dir'], 'workspace/youlun/')
    manage_file = os.path.join(youlun_workspace, 'manage.py')
    if os.path.exists(manage_file):
        with cd(youlun_workspace):
            try:
                #Step 2
                env.run('python manage.py sanitize')
                #Step 3
                db_export(dump_dst='',from_db='sanitized')
                push_dump(db=True,es=False)
            except Exception, e:
                logging.error("Sanitized database and push dump failed because %s", str(e))
    else:
        logging.error("File of manage_file: %s is not exist!" % manage_file)



if __name__ == '__main__':
    Run()