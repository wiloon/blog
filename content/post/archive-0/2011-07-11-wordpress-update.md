---
title: WordPress upgrade
author: "-"
type: post
date: 2011-07-11T14:36:49+00:00
url: /?p=341
bot_views:
  - 9
views:
  - 2
categories:
  - Wordpress

---
backup the mysql DB
  
#backup wordpress files /var/www/wordpress
  
zip -r /home/wiloon/tmp/wordpressBak.zip /var/www/wordpress

unzip new wordpress to /var/www/
  
cp  wp-config-sample.php wp-config.php
  
configure wp-config.php
  
DB_NAME
  
DB_USER
  
DB_PASSWORD

restart apache