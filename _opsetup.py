#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _opinstall import InstallWorker
from optparse import OptionParser
import os
import re
import subprocess
import sys
import shutil
import tempfile


class SetupWorker:

  def __init__(self, dir_name, target_version=None, repository=None, base_dir=os.getcwd()):
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
    p = subprocess.Popen(args, **subproc_args)
    result = p.wait()
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
    self.cp_config('ProjectConfiguration.class.php.sample', 'ProjectConfiguration.class.php')
    self.sed()

  def cp_config(self, src, target):
    shutil.copyfile(os.sep.join([self.get_target_dir_name(), 'config', src]), os.sep.join([self.get_target_dir_name(), 'config', target]));

  def sed(self):
    self.pat_replace('#RewriteBase', 'RewriteBase', os.sep.join([self.get_target_dir_name(), 'web', '.htaccess']))

  def pat_replace(self, stext, rtext, file):
    tmpfd, tmpname = tempfile.mkstemp(dir='.')
    try:
      output_file = os.fdopen(tmpfd, 'w')
      input_file = open(file)
      for line in input_file:
        a = line.replace(stext, rtext)
        output_file.write(a)
    finally:
      output_file.close()
      input_file.close()

    shutil.copyfile(tmpname, file)
    os.remove(tmpname)

  def get_target_dir_name(self):
    return self.base_dir + os.sep + self.dir_name

  def get_target_version(self):
    return self.target_version

  def get_repository(self):
    return self.repository


if __name__ == '__main__':
  parser = OptionParser()
  parser.add_option('-d', '--directory', dest='dir_name', metavar='DIR', help='name of target to setup')
  parser.add_option('-c', '--commit', dest='commit_name', metavar='COMMIT', help='commit of target to setup')
  parser.add_option('-b', '--branch', dest='branch_name', metavar='BRANCH', help='branch of target ot setup (not working)')
  parser.add_option('-r', '--repo', dest='repo', metavar='REPOSITORY', help='repository of target to setup', default='git://github.com/openpne/OpenPNE3.git')
  parser.add_option('-i', '--install', action='store_true', dest='is_install', help='set if you want to install')

  (options, args) = parser.parse_args();

  setup = SetupWorker(options.dir_name, options.commit_name, options.repo)
  print setup.get_target_dir_name()
  print setup.get_target_version()
  print setup.get_repository()
  print 'インストールする' if options.is_install else 'インストールしない'

  if options.dir_name == '':
    sys.exit(0)

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
    domain_name = setup.dir_name + '.domainname'
    database_name = 'openpne_' + re.sub(r'[.-]', '_', setup.dir_name)

    install = InstallWorker(domain_name, database_name, setup.get_target_dir_name())
    install.execute()

  #kexcept Exception:
  #k  print 'error'
