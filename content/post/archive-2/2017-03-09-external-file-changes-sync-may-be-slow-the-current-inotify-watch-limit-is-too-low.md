---
title: 'external file changes sync may be slow the current inotify  watch limit is too low'
author: wiloon
type: post
date: 2017-03-09T02:05:42+00:00
url: /?p=9906
categories:
  - Uncategorized

---
http://ggarcia.me/2016/07/12/intellij-inotify-arch.html

To fix the warning about **fs.inotify.max\_user\_watches** the IntelliJ shows, it is necessary to set a value for the **fs.inotify.max\_user\_watches** and then apply the change.

Here are the commands necessary to fix the issue on ArchLinux:

<div class="language-shell highlighter-rouge">
  <pre class="highlight"><code>sudo &lt;span class="nb">echo&lt;/span> &lt;span class="s1">'fs.inotify.max_user_watches = 524288'&lt;/span> &gt;&gt;/usr/lib/sysctl.d/50-default.conf
sudo sysctl -p --system
</code></pre>
</div>

More information about this can be found in <a href="https://confluence.jetbrains.com/display/IDEADEV/Inotify+Watches+Limit" target="_blank" rel="noopener noreferrer">here</a> and in <a href="https://bbs.archlinux.org/viewtopic.php?id=193020" target="_blank" rel="noopener noreferrer">here</a>.

&nbsp;

https://confluence.jetbrains.com/display/IDEADEV/Inotify+Watches+Limit