---
title: archlinux grub
author: wiloon
type: post
date: 2020-01-12T07:22:08+00:00
url: /?p=15345
categories:
  - Uncategorized

---
For parted set/activate the flag bios_grub on the partition.

<pre><code class="language-bash line-numbers">set 1 bios_grub on
pacman -S grub
grub-install --target=i386-pc /dev/sdX
grub-mkconfig -o /boot/grub/grub.cfg
</code></pre>