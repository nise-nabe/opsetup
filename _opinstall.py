#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys

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
            p = subprocess.Popen(args, **subproc_args)
            p.communicate('mysql\ndbuser\npassword\nlocalhost\n\n'
                          + self.database_name)
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
