#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
            home = os.environ['HOME']
            conf = ConfigParser.SafeConfigParser()
            conf.read(home + '/.openpne/database.conf')

            dbms = conf.get('prod' , 'dbms')
            dbusername = conf.get('prod' , 'username')
            dbpassword = conf.get('prod' , 'password')
            dbhostname = conf.get('prod' , 'hostname')
            dbportname = conf.get('prod' , 'port')
            dbsocket = conf.get('prod' , 'sock')

            p = subprocess.Popen(args, **subproc_args)
            p.communicate(dbms + '\n'
                    + dbusername + '\n'
                    + dbpassword + '\n'
                    + dbhostname + '\n'
                    + dbportname + '\n'
                    + self.database_name + '\n'
                    + dbsocket)
            ret = p.wait()
            print "Return code: %d" % ret
        except OSError:
            print "OpenPNE ディレクトリじゃなくね？"
            sys.exit(1)

if __name__ == '__main__':
    dirname = os.getcwd().split(os.sep)[-1]

    domain_name = dirname
    database_name = re.sub(r'[.-]', '_', dirname)

    print os.getcwd()
    print 'domain = ' + domain_name
    print 'database = ' + database_name

    while True:
        yn = raw_input('インストールしますか？ y/N: ')
        if re.compile('[yY]').match(yn):
            break
        elif re.compile('[nN]').match(yn):
            print 'aborted'
            sys.exit(0)

    install = InstallWorker(domain_name, database_name)
    install.execute()
