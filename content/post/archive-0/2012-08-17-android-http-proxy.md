---
title: android http proxy
author: w1100n
type: post
date: 2012-08-17T02:51:41+00:00
url: /?p=3905
categories:
  - Uncategorized

---
  
    I've connected my Android phone to my Wifi network at work, but they use a proxy and I cannot use my browser without setting the proxy on my browser. Is there any way I can do this?
  

<div id="post-749">
  The great thing about Android is that the operating system on your phone is open up to any tweaking you might want to do. unfortunately, there is no UI for proxy settings for Android web browser. Instead the Android web browser will read the proxy settings in its settings database. 
  
    Here are the instructions to enable the proxy in the android web browser.
  
  <ol>
    <li>
      > adb shell
    </li>
    <li>
      # sqlite3 /data/data/com.google.android.providers.settings/databases/settings.db
    </li>
    <li>
      sqlite> INSERT INTO system VALUES(99,'http_proxy', 'proxy:port');
    </li>
    <li>
      sqlite>.exit
    </li>
  </ol>
  
    You can talk to settings.db for more information.
  
  <ol>
    <li>
      sqlite> SELECT * FROM system;
    </li>
    <li>
      sqlite> .tables
    </li>
    <li>
      sqlite> .databases
    </li>
    <li>
      sqlite> .schema table_name
    </li>
    <li>
      sqlite> any SQL expressions to talk to the tables
    </li>
  </ol>
