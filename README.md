opsetup
=======

under construction

# How to Use

Setup database parameter

    $ mkdir ~/.openpne
    $ cp config/config.sample ~/.openpne/config
    $ vim ~/.openpne/config

Exec Example getting source and install

    $ _opsetup.py OpenPNE-3.8.1 381sns.example.com -i


Exec Example only install

this command use current directory's name to dbname replacing '.' or '-' to '\_'

    $ cd $OPENPNE_DIR
    $ _opinstall.py


You can deploy in /var/www/sns (default) using symlink as follow command:

    $ _opdeploy.py

# Server Setup

## Required

mod\_rewrite

mod\_vhost\_alias

## Settings

### Apache

if you write 'base\_domain=sns.example.com' and 'sns\_base\_dir=/var/www/sns' in config file,
you can use wild card domain setting as follow:

    <VirtualHost *:80>
      ServerName .sns.example.com
      ServerAlias *.sns.example.com
      Options -Indexes +FollowSymLinks
      VirtualDocumentRoot "/var/www/sns/%0/web"
    </VirtualHost>

### MySQL

if you write 'prefix=openpne' in config file, you can grant privileges as follow:

    mysql> grant all privileges on `openpne_%`.* to sns_user@'localhost' identified by '******';
