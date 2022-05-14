---
title: zentao
author: "-"
date: 2018-11-26T09:03:17+00:00
url: /?p=12937
categories:
  - inbox
tags:
  - reprint
---
## zentao
https://github.com/idoop/zentao
  
https://github.com/iboxpay/ldap

下载iboxpay/ldap 扩展, 作为插件安装。此插件会安装三个文件
  
    /opt/zentao/lib/ldap/ldap.class.php

    # ldap 配置
    /opt/zentao/module/user/ext/config/ldap.php
      
    /opt/zentao/module/user/ext/model/ldap.php

参照 https://blog.csdn.net/BigBoySunshine/article/details/80502068
  
修改
  
/opt/zentao/module/user/ext/config/ldap.php

```bash
  
$config->ldap->ldap_server
  
$config->ldap->ldap_root_dn
  
$config->ldap->ldap_bind_dn
  
$config->ldap->ldap_bind_passwd
  
```

/opt/zentao/lib/ldap/ldap.class.php

```bash
   
if ( @ldap_bind( $t_ds, "{$t_info[$i]['dn']}", $p_password ) ) {
  
```

/opt/zentao/module/user/js/login.js

```bash
    
if(password.length != 32 && typeof(md5) == 'function') $('input:password').val(password);
  
```