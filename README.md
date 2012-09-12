opsetup
=======

under construction

# How to Use

Setup database parameter

    $ mkdir ~/.openpne
    $ cp config/database.conf.sample ~/.openpne/database.conf
    $ vim ~/.openpne/database.conf

Exec Example getting source and install

    $ _opsetup.py -c OpenPNE-3.8.1 -d 381sns.example.com -i


Exec Example only install

this command use current directory's name to dbname replacing '.' or '-' to '\_'

    $ cd $OPENPNE_DIR
    $ _opinstall.py

# Server Setup

## Required

mod\_rewrite

mod\_vhost\_alias

## Settings

Apache

    <VirtualHost *:80>
      ServerName .aaa
      ServerAlias *.aaa
      Options -Indexes +FollowSymLinks
      VirtualDocumentRoot "/var/www/sns/%0/web"
    </VirtualHost>
