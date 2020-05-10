---
title: Unable to locate WordPress Content directory
author: wiloon
type: post
date: 2012-05-26T02:50:27+00:00
url: /?p=3240
categories:
  - Linux
  - Wordpress

---
Unable to locate WordPress Content directory (wp-content)

adding the following code in my wp-config.php:

[php]
  
if(is_admin()) {
  
add\_filter(&#8216;filesystem\_method&#8217;,
  
create_function(&#8216;$a&#8217;, &#8216;return "direct";&#8217; ));
  
define( &#8216;FS\_CHMOD\_DIR&#8217;, 0751 ); }
  
[/php]

如果提示没有写权限之类&#8230;

[shell]
  
chmod -R 777 /var/www/wordpress/wp-content/
  
[/shell]

http://wordpress.org/support/topic/unable-to-locate-wordpress-plugin-directory-1
  
http://jutang.blogbus.com/logs/106193937.html