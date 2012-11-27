#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _opinstall import InstallWorker
from optparse import OptionParser
import ConfigParser
import os
import re
import subprocess
import sys
import shutil
import tempfile


class SetupWorker:

    def __init__(self, dir_name, target_version=None,
                 repository=None, base_dir=os.getcwd()):
        self.dir_name = dir_name
        self.target_version = target_version
        self.repository = repository
        self.base_dir = base_dir

    def execute(self):
        self.get_src()
        self.change_version(self.target_version)
        self.setup_config_files()

    def get_src(self):
        subproc_args = { 'cwd': self.base_dir, 'close_fds': True }
        args = ['git', 'clone', self.repository, self.dir_name]
        proc = subprocess.Popen(args, **subproc_args)
        result = proc.wait()
        if result > 0:
            raise Exception


    def change_version(self, target_version=None):
        if target_version == None:
            target_version = self.target_version
        if self.target_version == None:
            return

        subproc_args = { 'cwd': self.get_target_dir_name(), 'close_fds': True }
        args = ['git', 'checkout', target_version]
        p = subprocess.Popen(args, **subproc_args)
        result = p.wait()
        if result > 0:
            raise Exception

    def setup_config_files(self):
        self.cp_config('OpenPNE.yml.sample', 'OpenPNE.yml')
        self.cp_config('ProjectConfiguration.class.php.sample',
                       'ProjectConfiguration.class.php')
        self.sed()

    def cp_config(self, src, target):
        src_dir = os.sep.join([self.get_target_dir_name(), 'config', src])
        tar_dir = os.sep.join([self.get_target_dir_name(), 'config', target])
        shutil.copyfile(src_dir, tar_dir)

    def sed(self):
        tar_dir = os.sep.join([self.get_target_dir_name(), 'web', '.htaccess'])
        self.pat_replace('#RewriteBase', 'RewriteBase', tar_dir)

    def pat_replace(self, stext, rtext, filename):
        tmpfd, tmpname = tempfile.mkstemp(dir='.')
        try:
            output_file = os.fdopen(tmpfd, 'w')
            input_file = open(filename)
            for line in input_file:
                a = line.replace(stext, rtext)
                output_file.write(a)
        finally:
            output_file.close()
            input_file.close()

        shutil.copyfile(tmpname, filename)
        os.remove(tmpname)

    def get_target_dir_name(self):
        return os.sep.join([self.base_dir, self.dir_name])

    def get_target_version(self):
        return self.target_version

    def get_repository(self):
        return self.repository


if __name__ == '__main__':
    usage = u'%prog [Version] [Directory] [Options]\nDetailed options -h or --help'
    parser = OptionParser(usage=usage, version=1.0)
    parser.add_option('-b', '--branch', dest='branch_name', metavar='BRANCH',
                      help='branch of target ot setup (not working)')
    parser.add_option('-r', '--repo', dest='repo', metavar='REPOSITORY',
                      help='repository of target to setup',
                      default='git://github.com/openpne/OpenPNE3.git')
    parser.add_option('-i', '--install', action='store_true', dest='is_install',
                      help='set if you want to install')
    parser.add_option('-f', '--force', action='store_true', dest='is_force',
                      help='set if you want to force setup')

    conf_file = os.sep.join([os.environ['HOME'], '.openpne', 'config'])
    conf = ConfigParser.SafeConfigParser()
    if not os.path.isfile(conf_file):
        print 'config file does not exist: ' + conf_file
        sys.exit(0)

    conf.read(conf_file)

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error('Argument is not enough')

    setup = SetupWorker(args[1], args[0], options.repo)

    domain_name = setup.dir_name
    base_domain = conf.get('web', 'base_domain')
    if base_domain != '':
        domain_name += '.' + base_domain
    db_prefix = conf.get('database', 'prefix')
    if db_prefix != '':
        db_prefix += '_'
    database_name = db_prefix + re.sub(r'[.-]', '_', domain_name)

    print 'dir: ' + setup.get_target_dir_name()
    print 'ver: ' + setup.get_target_version()
    print 'rep: ' + setup.get_repository()
    if options.is_install:
        print 'db: ' + database_name
        print 'インストールする'
    else:
        print 'インストールしない'

    if not options.is_force:
        while True:
            yn = raw_input('セットアップしますか？ y/N: ')
            if re.compile('[yY]').match(yn):
                break
            elif re.compile('[nN]').match(yn):
                print 'aborted'
                sys.exit(0)

    #try:
    setup.execute()

    if options.is_install:
        install = InstallWorker(domain_name, database_name,
                                setup.get_target_dir_name())
        install.execute()

    #kexcept Exception:
    #k  print 'error'
