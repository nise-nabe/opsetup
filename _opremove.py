#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import ConfigParser
import os
import re
import subprocess
import sys
import shutil

class RemoveWorker:

    def __init__(self, dir_name, database_name, base_dir=os.getcwd()):
        self.dir_name = dir_name
        self.database_name = database_name
        self.base_dir = base_dir

    def execute(self):
        subproc_args = { 'cwd': self.base_dir, 'close_fds': True }

        conf = ConfigParser.SafeConfigParser()
        conf.read(os.sep.join([os.environ['HOME'], '.openpne' , 'config']))

        args = ['mysqladmin',
                '--user=' + conf.get('database', 'username'),
                '--password=' + conf.get('database', 'password'),
                '--host=' + conf.get('database', 'hostname'),
                '--port=' + conf.get('database', 'port'),
                '-f', 'drop', self.database_name]
        p = subprocess.Popen(args, **subproc_args)
        ret = p.wait()
        print "DB Drop Return code: %d" % ret
        if ret == 0:
            shutil.rmtree(os.sep.join([self.base_dir, self.dir_name]),
                    False, (lambda: "Fail to remove sns dir"))


if __name__ == '__main__':
    usage = u'%prog [Directory] \nDetailed options -h or --help'
    parser = OptionParser(usage=usage, version=1.0)
    parser.add_option('-f', '--force', action='store_true', dest='is_force',
                      help='set if you want to force remove')

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error('Argument is not enough')

    conf = ConfigParser.SafeConfigParser()
    conf.read(os.sep.join([os.environ['HOME'], '.openpne' , 'config']))

    base_domain = conf.get('web', 'base_domain')
    if base_domain != '':
      base_domain = '.' + base_domain
    domain_name = args[0] + base_domain

    db_prefix = conf.get('database', 'prefix')
    if db_prefix != '':
        db_prefix += '_'
    database_name = db_prefix + re.sub(r'[.-]', '_', domain_name)

    print os.getcwd()
    print 'dir = ' + args[0]
    print 'database = ' + database_name

    if not options.is_force:
        while True:
            yn = raw_input('削除しますか？ y/N: ')
            if re.compile('[yY]').match(yn):
                break
            elif re.compile('[nN]').match(yn):
                print 'aborted'
                sys.exit(0)

    worker = RemoveWorker(args[0], database_name)
    worker.execute()
