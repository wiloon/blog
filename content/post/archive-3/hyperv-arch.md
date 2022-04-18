---
title: hyperv archlinux
author: "-"
date: 2019-04-01T06:53:10+00:00
url: /?p=14064

categories:
  - inbox
tags:
  - reprint
---
## hyperv archlinux

### hyper v 禁用安全启动

虚拟机>设置>安全>启用安全启动(去掉勾选)

### network

在虚拟机栏中右键点击虚拟机>设置>添加硬件  
选择"网络适配器"  
点击添加按钮  
添加 Default switch.  
Default switch默认会做nat,添加 后虚拟机可以正常访问网络.但Default switch的ip/网段每次重启会变,如果 需要 固定ip,需要另外手动新建一个交换机sw0  

#### 新建虚拟交换机

Hyper-V 管理器>右侧操作栏>虚拟交换机管理器>新建虚拟交换机>内部>新建虚拟交换机
名称: sw0
连接类型:  内部网络
在windows中打开网络适配器设置,手动设置sw的  
ip为 192.168.80.1  
网关可以不填  
dns: 192.168.1.xxx  

#### linux里

手动测试sw0的ip : 192.168.80.2
  
Gateway 不要设置, 两个网卡 对应default switch的设置默认网关,sw0不设置
  
DNS: 192.168.1.xxx

### 问题

遇到过一次虚拟机不能访问外网, 确认linux网络 配置没有问题, 重启windows解决了.

### install VcXsrv

### GUI

#### VSOCK + x410
<https://x410.dev/cookbook/hyperv/using-x410-with-hyper-v-linux-virtual-machines-via-vsock/>

##### 卸载 xrdp

    yay -R xrdp

##### 修改win10注册表,配置vsock

x410-display-0-only.reg

    Windows Registry Editor Version 5.00

    [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\GuestCommunicationServices\00001770-facb-11e6-bd58-64006a7986d3]
    "ElementName"="X410 Display 0"

##### 启动x410 并 开启vsock

    x410 /listen hyperv /desktop

##### xfce4 桌面启动脚本

sudo vim /usr/bin/start-xfce4-desktop.sh
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP="XFCE"
exec startxfce4

##### 用socat 测试vsock

    pacman -S socat
    socat -b65536 UNIX-LISTEN:/tmp/.X11-unix/X0,fork,mode=777 SOCKET-CONNECT:40:0:x0000x70170000x02000000x00000000 &
    export DISPLAY=:0.0
    # startxfce4
    start-xfce4-desktop.sh
    # x410 窗口里应该能看到xfce4桌面了

##### socat 作为服务启动

    vim /etc/systemd/system/x410vsock.service
    #---
    [Unit]
    Description=X410 VSOCK Service
    After=network.target

    [Service]
    User=root
    Restart=always
    Type=simple
    ExecStart=/usr/bin/socat -b65536 UNIX-LISTEN:/tmp/.X11-unix/X0,fork,mode=777 SOCKET-CONNECT:40:0:x0000x70170000x02000000x00000000

    [Install]
    WantedBy=multi-user.target

##### 自动登录tty2

    sudo vim /etc/systemd/system/x410tty.service
    #---
    [Unit]
    Description=X410 Autologin Service
    After=network.target x410vsock.service

    [Service]
    User=root
    Restart=always
    Type=simple
    ExecStart=-/sbin/agetty --autologin <user0> --noclear tty2 $TERM

    [Install]
    WantedBy=multi-user.target

##### shell 登录后启动桌面

    vim ~/.zshrc
    if [[ ! $DISPLAY && -S "/tmp/.X11-unix/X0" ]]; then
        export DISPLAY=:0.0
    if [[ $XDG_VTNR -eq 2 ]]; then
        exec /usr/bin/start-xfce4-desktop.sh
    fi
    fi

##### 把socat, tty 设置成开机启动

    sudo systemctl enable x410vsock.service
    sudo systemctl enable x410tty.service

##### 重启虚拟机

    sudo reboot

#### VcXsrv

    vim .bashrc
    export DISPLAY=192.168.80.1:0
    startxfce4

### hyperv service

    pacman -S hyperv
    systemctl enable  hv_fcopy_daemon.service
    systemctl enable  hv_kvp_daemon.service
    systemctl enable  hv_vss_daemon.service

### Internal switch
  
### Xorg

    pacman -S xf86-video-fbdev

```bash
/boot/loader/entries/arch.conf
title Arch Linux
linux /vmlinuz-linux
initrd /initramfs-linux.img
options video=hyperv_fb:1920x1080 root=PARTUUID=xxxx-xxxx rw
```

#### Enhanced Session Mod

    git clone https://github.com/Microsoft/linux-vm-tools
    cd linux-vm-tools/arch
    ./makepkg.sh
    ./install-config.sh

    yay -S xrdp
    sudo systemctl enable xrdp.service 
    sudo systemctl enable xrdp-sesman.service

#### ~/.xinitrc

    exec startxfce4

#### 以管理员身份运行powershell 并执行

    Set-VM -VMName arch -EnhancedSessionTransportType HvSocket

<https://wiki.archlinux.org/index.php/Hyper-V>
<https://x410.dev/cookbook/command-line-switches/>
