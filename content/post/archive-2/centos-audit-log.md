---
title: centos audit.log
author: "-"
date: 2018-09-25T02:02:50+00:00
url: /?p=12690
categories:
  - Uncategorized

---
## centos audit.log
```bash
  
ansible all -m yum -a 'name=audit state=present'
  
ansible all -m yum -a 'name=audit-libs state=present'
  
ansible all -m service -a 'name=auditd state=restarted'

```