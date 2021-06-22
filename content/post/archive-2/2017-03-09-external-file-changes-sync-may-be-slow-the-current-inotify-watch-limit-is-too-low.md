---
title: 'external file changes sync may be slow the current inotify  watch limit is too low'
author: "-"
type: post
date: 2017-03-09T02:05:42+00:00
url: /?p=9906
categories:
  - Uncategorized

---
http://ggarcia.me/2016/07/12/intellij-inotify-arch.html

To fix the warning about **fs.inotify.max_user_watches** the IntelliJ shows, it is necessary to set a value for the **fs.inotify.max_user_watches** and then apply the change.

Here are the commands necessary to fix the issue on ArchLinux:

<div class="language-shell highlighter-rouge">
  <pre class="highlight"><code>sudo <span class="nb">echo <span class="s1">'fs.inotify.max_user_watches = 524288' >>/usr/lib/sysctl.d/50-default.conf
sudo sysctl -p --system
```

More information about this can be found in <a href="https://confluence.jetbrains.com/display/IDEADEV/Inotify+Watches+Limit" target="_blank" rel="noopener noreferrer">here</a> and in <a href="https://bbs.archlinux.org/viewtopic.php?id=193020" target="_blank" rel="noopener noreferrer">here</a>.


https://confluence.jetbrains.com/display/IDEADEV/Inotify+Watches+Limit