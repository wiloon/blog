---
title: fstab
author: "-"
date: 2017-08-10T01:15:57+00:00
url: fstab
categories:
  - Linux
tags:
  - Linux

---
## fstab

### 格式

```bash
<file system> <dir> <type> <options> <dump> <pass>
```

### 示例

```bash
UUID=48ab4d71-5bb2-4bc4-bf32-dc357020ae27       /data   ext4    defaults        0       0
UUID=b256c0bb-9000-456b-b9eb-18239b5df5ddswap   none    swap    defaults        0       0
UUID=E854-F511  /boot   vfat    rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,utf8,errors=remount-ro   0       2

# 支持TRIM 的ssd 启用trim, 在参数里加discard, 使用discard受系统和硬件限制, 大多数系统建议后台服务定时discard, 如:  fstrim.timer
/dev/sdb1  /data1       ext4   defaults,noatime,discard   0  0
```

<https://wiki.archlinux.org/index.php/Fstab_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87>)

- `<options>`
挂载时使用的参数，注意有些 参数是特定文件系统才有的。
  - defaults -  使用文件系统的默认挂载参数，例如 ext4 的默认参数为:rw, suid, dev, exec, auto, nouser, async.
  - rw - 以读写模式挂载文件系统。
  - relatime - 实时更新 inode access 记录。只有在记录中的访问时间早于当前访问才会被更新。 (与 noatime 相似，但不会打断如 mutt 或其它程序探测文件在上次访问后是否被修改的进程。），可以提升性能(参见 atime 参数)。
  - fmask - 设置文件的权限过滤, dmask和fmask是mount的选项，针对fat/ntfs文件系统，适用于fstab配置, 通过设置 fmask, dmask, uid, gid参数可以控制文件目录的默认权限以及所属用户和组。
  - dmask —— 设置目录的权限过滤
  - iocharset
  - codepage

Sets the codepage for converting to shortname characters on FAT and VFAT filesystems. By default, codepage 437 is used.
源自 MS-DOS 或者 Windows 的文件系统 (例如：vfat、ntfs、smbfs、cifs、iso9660、udf) 需要使用挂载选项 “iocharset” 使得文件名中的非 ASCII 字符能够正确转码。此选项的值应设置为与你的区域数据的字符集相同，使得内核能够理解。如果对应的字符集定义 (位于 File systems -> Native Language Support，即文件系统 -> 原生语言支持) 编译到内核中或者编制成模块，它就能工作。vfat 和 smbfs 文件系统还需要 “codepage” 选项。它应该设置为你所在的国家在 MS-DOS 下使用的 codepage 号码。例如，为了挂载优盘，zh_CN.GB2312 用户的 /etc/fstab 文件中会需要：

noauto,user,quiet,showexec,iocharset=gb2312,codepage=936

- shortname={ lower| win95| winnt| mixed}
Defines the behaviour for creation and display of filenames which fit into 8.3 characters. If a long name for a file exists, it will always be preferred display. There are four modes: :
lower
Force the short name to lower case upon display; store a long name when the short name is not all upper case. This mode is the default.

win95

Force the short name to upper case upon display; store a long name when the short name is not all upper case.

winnt

Display the shortname as is; store a long name when the short name is not all lower case or all upper case.

mixed

Display the short name as is; store a long name when the short name is not all upper case.

- errors={continue|remount-ro|panic}
Define the behavior when an error is encountered. (Either ignore errors and just mark the filesystem erroneous and continue, or remount the filesystem read-only, or panic and halt the system.) The default is set in the filesystem superblock, and can be changed using tune2fs(8).

定义遇到错误时的行为。

 (要么忽略错误，只是标记文件系统错误并继续，或者重新挂载文件系统为只读，或者panic并停止系统）

默认设置在文件系统超级块中，可以使用tune2fs (8）进行更改。

- `<dump>`
dump 工具通过它决定何时作备份. dump 会检查其内容,并用数字来决定是否对这个文件系统进行备份。 允许的数字是 0 和 1 。0 表示忽略, 1 则进行备份。大部分的用户是没有安装 dump 的 ,对他们而言 `<dump>` 应设为 0。

- `<pass>`
`<pass>` fsck 读取 `<pass>` 的数值来决定需要检查的文件系统的检查顺序。允许的数字是0, 1, 和2。 根目录应当获得最高的优先权 1, 其它所有需要被检查的设备设置为 2. 0 表示设备不会被 fsck 所检查。


>https://blog.csdn.net/qq_24884901/article/details/90639143