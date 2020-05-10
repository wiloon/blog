---
title: wordpress install
author: wiloon
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

CREATE USER wordpress IDENTIFIED BY &#8216;PASSWORD&#8217;

grant all privileges on wordpress.* to wordpress@localhost;

#install wordpress

download the latest version of wordpress

#<a id="" href="http://wordpress.org/" shape="rect" target="_blank">http://wordpress.org/</a>

extract and move to /var/www/

cd wordpress

sudo cp wp-config-sample.php wp-config.php

#edit wp-config.php

define(&#8216;DB_NAME&#8217;, &#8216;wordpress&#8217;);    // The name of the database

define(&#8216;DB_USER&#8217;, &#8216;username&#8217;);     // Your MySQL username

define(&#8216;DB_PASSWORD&#8217;, &#8216;password&#8217;); // &#8230;and password

#import wordpress DB data

#restart apache

#wordpress login url:<a id="" href="http://www.wiloon.com/wordpress/wp-login.php" shape="rect" target="_blank">http://www.wiloon.com/wordpress/wp-login.php</a>

#Go to browser check the wordpress is ok&#8230;