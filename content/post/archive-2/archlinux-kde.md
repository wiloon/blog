---
title: archlinux kde, config
author: "-"
date: 2018-06-11T10:48:46+00:00
url: kde
tags:
  - kde

---
## archlinux kde, config
```bash
sudo pacman -S xorg xorg-xinit
sudo pacman -S plasma-desktop
echo "exec startplasma-x11" > ~/.xinitrc

sudo pacman -S konsole dolphin kate
startx
sudo pacman -S sddm
sudo pacman -S breeze-gtk breeze kde-gtk-config
sudo pacman -S kdeplasma-addons

sudo pacman -S kwalletmanager
# start kwalletmanager and disactive kwallet
```

### 登录后启动kde
```bash
vim /home/wiloon/.zshrc
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  exec startx
fi
```

[https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login][1]{.wp-editor-md-post-content-link}

sddm
  
https://wiki.archlinux.org/index.php/Display_manager#Loading_the_display_manager

 [1]: https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login "https://wiki.archlinux.org/index.php/Xinit#Autostart_X_at_login"

 ### 锁屏界面的日期时间格式
 https://chubuntu.com/questions/28565/how-to-display-kde-lock-screen-time-in-24-hour-format.html
 ```bash
vim  /usr/share/plasma/look-and-feel/org.kde.breeze.desktop/contents/components/Clock.qml
找到这一行: 

text: Qt.formatTime(timeSource.data["Local"]["DateTime"])
并将其更改为

text: Qt.formatTime(timeSource.data["Local"]["DateTime"], "hh:mm:ss")
对于ISO日期更改,请找到以下行: 

text: Qt.formatDate(timeSource.data["Local"]["DateTime"], Qt.DefaultLocaleLongDate);
并将其更改为

text: Qt.formatDate(timeSource.data["Local"]["DateTime"], "yyyy-MM-dd");
保存更改。

按Ctrl + Alt + L锁定屏幕并立即查看更改。
 ```

 ### kde 配置
 #### 多显示器
 Right-click on the background of the second screen -> Add Panel -> Empty Panel 
 add widgets: task manager