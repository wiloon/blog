---
title: wordpress install
author: w1100n
type: post
date: 2012-05-23T13:28:46+00:00
url: /?p=3184
categories:
  - Wordpress

---
#install apache

sudo apt-get install apache2

sudo apt-get install libapache2-mod-php5 php5

#install mysql

sudo apt-get install mysql-server

#mysql-common, mysql-admin (optional)

sudo apt-get install mysql-common mysql-admin

sudo apt-get install php5-mysql

#create DB for wordpress

CREATE DATABASE wordpress;

CREATE USER wordpress IDENTIFIED BY 'PASSWORD'

grant all privileges on wordpress.* to wordpress@localhost;

#install wordpress

download the latest version of wordpress

#<a id="" href="http://wordpress.org/" shape="rect" target="_blank">http://wordpress.org/</a>

extract and move to /var/www/

cd wordpress

sudo cp wp-config-sample.php wp-config.php

#edit wp-config.php

define('DB_NAME', 'wordpress');    // The name of the database

define('DB_USER', 'username');     // Your MySQL username

define('DB_PASSWORD', 'password'); // ...and password

#import wordpress DB data

#restart apache

#wordpress login url:<a id="" href="http://www.wiloon.com/wordpress/wp-login.php" shape="rect" target="_blank">http://www.wiloon.com/wordpress/wp-login.php</a>

#Go to browser check the wordpress is ok...