---
title: ansible create file
author: "-"
date: 2018-01-25T04:42:29+00:00
url: /?p=11786
categories:
  - Inbox
tags:
  - reprint
---
## ansible create file

```bash
  
- name: ensure file exists
    
copy:
      
content: ""
      
dest: /etc/nologin
      
force: no
      
group: sys
      
owner: root
      
mode: 0555
  
```

<https://stackoverflow.com/questions/28347717/how-to-create-an-empty-file-with-ansible>
