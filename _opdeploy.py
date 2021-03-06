#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ConfigParser

if __name__ == '__main__':
    conf = ConfigParser.SafeConfigParser()
    conf.read(os.sep.join([os.environ['HOME'], '.openpne' , 'config']))

    dirname = os.getcwd().split(os.sep)[-1]
    base_domain = conf.get('web', 'base_domain')
    if base_domain != '':
      base_domain = '.' + base_domain

    domain_name = dirname + base_domain
    target = os.sep.join([conf.get('web', 'sns_base_dir'), domain_name])
    print os.getcwd()
    print target
    os.symlink(os.getcwd(), target)
