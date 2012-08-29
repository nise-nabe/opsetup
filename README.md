opsetup
=======

under construction

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

# TODO

extract settings to files
