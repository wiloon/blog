---
title: zentao
author: "-"
date: 2018-11-26T09:03:17+00:00
url: zentao
categories:
  - inbox
tags:
  - reprint
aliases:
  - /p333/
  - /p1627/
  - /p3854/
  - /p4142/
  - /p8547/
  - /p8779/
  - /p8863/
  - /p8928/
  - /p8956/
  - /p9128/
  - /p9145/
  - /p9168/
  - /p9283/
  - /p9466/
  - /p9468/
  - /p9474/
  - /p9487/
  - /p9494/
  - /p9501/
  - /p9510/
  - /p9513/
  - /p9519/
  - /p9546/
  - /p9678/
  - /p9772/
  - /p9873/
  - /p9901/
  - /p9951/
  - /p9968/
  - /p10153/
  - /p10215/
  - /p10262/
  - /p11023/
  - /p11223/
  - /p11379/
  - /p11464/
  - /p11649/
  - /p11717/
  - /p11768/
  - /p12158/
  - /p12316/
  - /p12358/
  - /p12444/
  - /p12697/
  - /p12937/
  - /p13791/
  - /p13866/
  - /p13932/
  - /p14245/
  - /p14420/
  - /p14635/
  - /p14684/
  - /p14754/
  - /p14926/
  - /p14975/
  - /p15083/
  - /p15149/
  - /p15272/
  - /p15779/
  - /p16015/
  - /p16053/
  - /p16076/
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

## 禅道 docker + ldap插件
checkout https://github.com/idoop/zentao

修改docker-compose.yaml

修改MySQL端口

修改volumns路径

download ldap as zip https://github.com/iboxpay/ldap

参照https://github.com/iboxpay/ldap 的readme安装插件