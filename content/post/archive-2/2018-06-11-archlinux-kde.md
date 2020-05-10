---
title: archlinux kde
author: wiloon
type: post
date: 2018-06-11T10:48:46+00:00
url: /?p=12297
categories:
  - Uncategorized

---
<pre><code class="language-shell line-numbers">sudo pacman -S xorg xorg-xinit
echo "exec startplasma-x11" &gt; ~/.xinitrc
sudo pacman -S plasma-desktop
sudo pacman -S konsole dolphin kate
startx
sudo pacman -S sddm
sudo pacman -S breeze-gtk breeze kde-gtk-config
sudo pacman -S kdeplasma-addons

sudo pacman -S kwalletmanager
# start kwalletmanager and disactive kwallet
</code></pre>

### 登录后启动kde

<pre><code class="language-shell line-numbers">vim /home/wiloon/.zshrc
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi

</code></pre>

[https://wiki.archlinux.org/index.php/Xinit#Autostart\_X\_at_login][1]{.wp-editor-md-post-content-link}

sddm
  
https://wiki.archlinux.org/index.php/Display\_manager#Loading\_the\_display\_manager

 [1]: https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login "https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login"