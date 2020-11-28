---
title: Unable to locate WordPress Content directory
author: w1100n
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
  
add\_filter('filesystem\_method',
  
create_function('$a', 'return "direct";' ));
  
define( 'FS\_CHMOD\_DIR', 0751 ); }
  
[/php]

如果提示没有写权限之类...

```bash
  
chmod -R 777 /var/www/wordpress/wp-content/
  
```

http://wordpress.org/support/topic/unable-to-locate-wordpress-plugin-directory-1
  
http://jutang.blogbus.com/logs/106193937.html