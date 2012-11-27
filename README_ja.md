opsetup
=======

開発中

# How to Use

データベース設定を記述してください．

    $ mkdir ~/.openpne
    $ cp config/config.sample ~/.openpne/config
    $ vim ~/.openpne/config

ソースを取得してきてインストール作業まで行うには以下のように実行します．

    $ _opsetup.py OpenPNE-3.8.1 381sns.example.com -i

インストールのみを行うには以下のように実行します．

このコマンドはカレントディレクトリの '.' や '-' を '_' に置換したものを使います．

    $ cd $OPENPNE_DIR
    $ _opinstall.py

単に /var/www/sns （デフォルト）にシンボリックリンクを貼るだけをデプロイとするならば以下のように実行します．

    $ _opdeploy.py

# Server Setup

## Required

mod\_rewrite

mod\_vhost\_alias

## Settings

### Apache

データベースの設定に'base\_domain=sns.example.com' や 'sns\_base\_dir=/var/www/sns'と書いた場合は下記のような設定をすることができます．

    <VirtualHost *:80>
      ServerName .sns.example.com
      ServerAlias *.sns.example.com
      Options -Indexes +FollowSymLinks
      VirtualDocumentRoot "/var/www/sns/%0/web"
    </VirtualHost>

### MySQL

設定ファイルに 'prefix=openpne' のように書いているならば，下記のようなコマンドで openpne_ とついているデータベースにのみ操作を許可する権限を与えることができます．

    mysql> grant all privileges on `openpne_%`.* to sns_user@'localhost' identified by '******';
