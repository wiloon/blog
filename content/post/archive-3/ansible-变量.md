---
title: ansible 变量
author: "-"
date: 2019-10-21T09:04:49+00:00
url: /?p=15036
categories:
  - Inbox
tags:
  - reprint
---
## ansible 变量
ram_size: "{{ (ansible_memtotal_mb * 0.8)|int }}"