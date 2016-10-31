# *.* coding: utf-8 *.*
"""
SELECT DISTINCT CONCAT('User: ''',user,'''@''',host,''';') AS query FROM mysql.user;
show grants for 'ecom'@'%';
"""

import MySQLdb
import config

db=MySQLdb.connect(host=config.DB_HOST,user=config.DB_Adm,passwd=config.DB_Adm_PASS)
cursor = db.cursor()
sqllists = {}
sqllists['create_db'] =  'CREATE DATABASE %s' % config.DB_NAME
sqllists['create_user'] = "CREATE USER '%s\'@'%%' IDENTIFIED BY '%s'" % (config.DB_USER, config.DB_US_PASS)
sqllists['grant_user'] = "GRANT all privileges ON %s.* TO '%s'@'%%'" % (config.DB_NAME,config.DB_USER)
