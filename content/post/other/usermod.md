---
title: usermod
author: "-"
date: 2013-12-01T11:58:41+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: usermod
categories:
  - Linux
tags:
  - Linux
  - remix
  - AI-assisted
aliases:
  - /p6003/
---
## usermod

```bash
# add user to docker group
sudo usermod -aG docker $USER
```

禁止用户登录
  
```bash
usermod -s /sbin/nologin user0
```

应用举例:
  
1. 将 newuser2 添加到组 staff 中

```bash
usermod -G staff newuser2
```

2. 修改 newuser 的用户名为 newuser1

```bash
usermod -l newuser1 newuser
```

3. 锁定账号 newuser1

```bash
usermod -L newuser1
```

4. 解除对 newuser1 的锁定

```bash
usermod -U newuser1
```

功能说明: 修改用户帐号。

语法:

```text
usermod [-LU][-c <备注>][-d <登入目录>][-e <有效期限>][-f <缓冲天数>][-g <群组>][-G <群组>][-l <帐号名称>][-s <shell>][-u <uid>][用户帐号]
```

补充说明: usermod可用来修改用户帐号的各项设定。

参数:
  
- `-a` append
- `-c<备注>` 修改用户帐号的备注文字。
- `-d<登入目录>` 修改用户登入时的目录。
- `-e<有效期限>` 修改帐号的有效期限。
- `-f<缓冲天数>` 修改在密码过期后多少天即关闭该帐号。
- `-g<群组>` 修改用户所属的群组。
- `-G<群组>` 修改用户所属的附加群组。
- `-l<帐号名称>` 修改用户帐号名称。
- `-L` 锁定用户密码,使密码无效。
- `-s<shell>` 修改用户登入后所使用的shell。
- `-u<uid>` 修改用户ID。
- `-U` 解除密码锁定。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；categories 改为 Linux | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
