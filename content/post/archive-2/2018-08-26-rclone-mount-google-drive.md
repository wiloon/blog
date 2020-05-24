---
title: rclone mount google drive, webdav, onedrive
author: wiloon
type: post
date: 2018-08-26T10:32:10+00:00
url: /?p=12568
categories:
  - Uncategorized

---
### install rclone

```bash# install rclone
sudo pacman -S rclone
sudo pacman -S fuse
```

### config fuse

```bashsudo vim /etc/fuse.conf
# uncomment  user_allow_other
```

### google drive

```bash# config rclone
rclone config
# n, new config
# name? name-foo, a name
# 11, google drive
# client id, leave blank
# client secret, leave blank
# 1, full access
# root_folder_id, get from https://drive.google.com/drive/folders/
# service_account_file, leave blank
# Edit advanced config? (y/n) n
# auto config? y
# team drive? y
# y) Yes this is OK, y
# q) Quit config, q
rclone mount name-foo:path/to/files /path/to/local/mount --allow-other --vfs-cache-mode writes
```

```bashrclone lsl foo:
rclone dedupe --dedupe-mode newest $name

# linux mount google drive
rclone mount foo: /path/to/mount/point --allow-other --vfs-cache-mode writes

# windows mount google drive
rclone.exe mount foo:/ x: --cache-dir C:\path\to\cache\dir --vfs-cache-mode writes
# foo: google drive rclone name
# x: 挂载到的系统盘符
# --cache-dir C:\path\to\cache\dir, 缓存目录
```

### mount webdav

```bashrclone config
n
name0 # enter name
24 #webdav, see help at https://rclone.org/webdav/
#enter webdav url

#列出目录内容
# 注意： rclone 挂载点名字后面有冒号
rclone lsl
```

### mount via systemd

uid=1000, gid=2000

```bashsudo vim /etc/systemd/system/rclone.service

[Unit]
Description=keepass@foo
AssertPathIsDirectory=/mnt/keepassxc-db
After=docker.service

[Service]
Type=simple
ExecStart=/usr/bin/rclone mount \
        --config=/home/user0/.config/rclone/rclone.conf \
        --allow-other \
        --cache-tmp-upload-path=/tmp/rclone/upload \
        --cache-chunk-path=/tmp/rclone/chunks \
        --cache-workers=8 \
        --cache-writes \
        --cache-dir=/tmp/rclone/vfs \
        --cache-db-path=/tmp/rclone/db \
        --no-modtime \
        --drive-use-trash \
        --stats=0 \
        --checkers=16 \
        --bwlimit=40M \
        --dir-cache-time=60m \
        --cache-info-age=60m \
        --uid=1000 \
        --gid=2000 \
        --dir-perms=770 \
        --file-perms=770 \
        rclone_mount_name_0:/ /mnt/keepassxc-db --vfs-cache-mode writes
ExecStop=/bin/fusermount -u /mnt/mnt/keepassxc-db
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

https://rclone.org/webdav/

<blockquote class="wp-embedded-content" data-secret="JYXAHPlYuh">
  <p>
    <a href="https://www.jamescoyle.net/how-to/3116-rclone-systemd-startup-mount-script">rclone Systemd startup mount script</a>
  </p>
</blockquote>

<iframe title="&#8220;rclone Systemd startup mount script&#8221; &#8212; JamesCoyle.net Limited" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://www.jamescoyle.net/how-to/3116-rclone-systemd-startup-mount-script/embed#?secret=JYXAHPlYuh" data-secret="JYXAHPlYuh" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

### windows

for windows, install winfsp <https://github.com/billziss-gh/winfsp> first
  
windows vbs脚本后台挂载

<pre><code class="language-shell line-numbers">著作权归作者所有。
商业转载请联系作者获得授权，非商业转载请注明出处。
作者：Rhilip
链接：https://blog.rhilip.info/archives/874/
来源：https://blog.rhilip.info/

Option Explicit
Dim WMIService, Process, Processes, Flag, WS
Set WMIService = GetObject("winmgmts:{impersonationlevel=impersonate}!\\.\root\cimv2")
Set Processes = WMIService.ExecQuery("select * from win32_process")
Flag = true
for each Process in Processes
    if strcomp(Process.name, "rclone.exe") = 0 then
        Flag = false
        exit for
    end if
next
Set WMIService = nothing
if Flag then
    Set WS = Wscript.CreateObject("Wscript.Shell")
    WS.Run "rclone.exe mount foo:/ x: --cache-dir C:\path\to\cache\dir --vfs-cache-mode writes", 0
end if
```

### linux mount onedrive

<https://rclone.org/onedrive/>

```bashrclone config
storage&gt; 23
client_id&gt; ""
client_secret&gt; ""
dit advanced config? (y/n) n
Use auto config? y
Choose a number from below, or type in an existing value: 1 / OneDrive Personal or Business
Found 1 drives, please select the one you want to use: 0
Is that okay? y
y) Yes this is OK (default)
```

```bashsudo -i
rclone config
# ...
rclone mount onedrive-keepassxc-db:/keepassxc /mnt/ms-one-drive --copy-links --no-gzip-encoding --no-check-certificate --allow-other --allow-non-empty --umask 000
rclone mount onedrive: /mnt/ms-one-drive --allow-other
```

#### systemd config

```bashsudo vim  /etc/systemd/system/rclone-onedrive.service

[Unit]
Description=keepass@onedrive
AssertPathIsDirectory=/mnt/ms-one-drive
After=docker.service

[Service]
User=wiloon
Group=wiloon
Type=simple
ExecStart=/usr/bin/rclone mount onedrive-keepassxc-db: /mnt/ms-one-drive --allow-other --uid=1000 --gid=2000 --vfs-cache-mode writes
ExecStop=/bin/fusermount -u /mnt/ms-one-drive
Restart=always
RestartSec=10

[Install]
WantedBy=default.target

```

https://blog.rhilip.info/archives/874/
  
https://rclone.org/drive/
  
https://rclone.org/commands/rclone_mount/