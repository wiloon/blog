---
title: ansible playbook
author: wiloon
type: post
date: 2018-12-20T02:20:44+00:00
url: /?p=13156
categories:
  - Uncategorized

---
定义变量 - 列表

<pre><code class="language-yaml line-numbers">- hosts: localhost
  become: true
  vars:
    app_list:
      - - htop
        - emacs
        - vim
```

```bashansible-playbook /etc/ansible/xxx.yml --limit 192.168.xxx.xxx --tags "tag0,tag1" --list-hosts --list-tasks
--skip-tags
--start-at-task
--step # one-step-at-a-time: confirm each task before running

```