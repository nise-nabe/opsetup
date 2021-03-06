#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import re
import subprocess
import sys
import ConfigParser

class InstallWorker:

    def __init__(self, domain_name, database_name, base_dir=os.getcwd()):
        self.domain_name = domain_name
        self.database_name = database_name
        self.base_dir = base_dir

    def execute(self):
        subproc_args = { 'cwd': self.base_dir, 'stdin': subprocess.PIPE,
                         'close_fds': True }
        args = ['./symfony', 'openpne:install']
        try:
            conf = ConfigParser.SafeConfigParser()
            conf.read(os.sep.join([os.environ['HOME'], '.openpne' , 'config']))

            p = subprocess.Popen(args, **subproc_args)
            p.communicate('\n'.join([
                conf.get('database' , 'dbms'),
                conf.get('database' , 'username'),
                conf.get('database' , 'password'),
                conf.get('database' , 'hostname'),
                conf.get('database' , 'port'),
                self.database_name,
                conf.get('database' , 'sock'),
            ]))
            return p.wait()
        except OSError:
            return -1

if __name__ == '__main__':
    dirname = os.getcwd().split(os.sep)[-1]

    usage = u'%prog \nDetailed options -h or --help'
    parser = OptionParser(usage=usage, version=1.0)
    parser.add_option('-f', '--force', action='store_true', dest='is_force',
                      help='set if you want to force setup')

    conf = ConfigParser.SafeConfigParser()
    conf.read(os.sep.join([os.environ['HOME'], '.openpne' , 'config']))

    base_domain = conf.get('web', 'base_domain')
    if base_domain != '':
      base_domain = '.' + base_domain

    domain_name = dirname + base_domain
    db_prefix = conf.get('database', 'prefix')
    if db_prefix != '':
        db_prefix += '_'

    database_name = db_prefix + re.sub(r'[.-]', '_', domain_name)

    print os.getcwd()
    print 'domain = ' + domain_name
    print 'database = ' + database_name

    (options, args) = parser.parse_args()
    if not options.is_force:
      while True:
          yn = raw_input('インストールしますか？ y/N: ')
          if re.compile('[yY]').match(yn):
              break
          elif re.compile('[nN]').match(yn):
              print 'aborted'
              sys.exit(0)

    install = InstallWorker(domain_name, database_name)
    ret = install.execute()
    print "Return code: %d" % ret
