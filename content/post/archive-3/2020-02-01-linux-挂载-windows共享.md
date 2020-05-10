---
title: linux 挂载 windows共享
author: wiloon
type: post
date: 2020-02-01T02:25:40+00:00
url: /?p=15463
categories:
  - Uncategorized

---
先在 Windows 下面共享需要挂载的目录

<pre><code class="language-bash line-numbers">sudo mount -t cifs -o username=&lt;username&gt;,password=&lt;password&gt; //192.168.50.104/path/to/win/share /mnt/path/to/linux/mnt/dir
# windows域控账户不需要加前缀，直接写用户名

# 查看挂载状态
df -h

# 卸载
umount /mnt/path/to/linux/mnt/dir
</code></pre>

https://blog.csdn.net/tojohnonly/article/details/71374984