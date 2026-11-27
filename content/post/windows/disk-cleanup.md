---
title: Windows 硬盘空间清理
author: "-"
date: 2026-06-02T23:04:00+08:00
lastmod: 2026-06-02T23:04:00+08:00
url: windows-disk-cleanup

categories:
  - windows
tags:
  - windows
  - remix
  - AI-assisted
---

## 临时文件目录

### `C:\Users\<用户名>\AppData\Local\Temp`

存放应用程序运行时产生的临时文件，目录里的文件可以安全删除。

**手动清理**：

在文件资源管理器地址栏输入 `%LOCALAPPDATA%\Temp` 回车，全选并删除。

或者在"运行"对话框（`Win + R`）中输入 `%temp%`，回车后打开目录，全选删除。

部分文件可能正被程序占用无法删除，跳过即可，不影响系统运行。

**使用磁盘清理工具**：

`Win + R` 输入 `cleanmgr`，选择要清理的驱动器，勾选"临时文件"后确认。

### `C:\Windows\Temp`

系统级临时文件目录，需要管理员权限才能清理。全选删除，跳过被占用的文件即可。

### `C:\Windows\SoftwareDistribution\Download`

Windows Update 下载缓存。更新安装完成后，这里的文件可以删除，不影响已安装的更新。

清理前建议先停止 Windows Update 服务：

```bat
net stop wuauserv
```

删除目录内容后再启动服务：

```bat
net start wuauserv
```

### `C:\Windows.old`

Windows 大版本升级后保留的旧系统文件，通常占用数 GB 到十几 GB。

升级后 10 天内系统会自动保留用于回滚，确认新系统稳定后可通过磁盘清理工具删除：`cleanmgr` → 清理系统文件 → 勾选"以前的 Windows 安装"。

### 回收站

右键桌面回收站图标 → 清空回收站。

### `C:\Users\<用户名>\Downloads`

下载目录积累的安装包、压缩包等，手动检查后删除不再需要的文件。

### 缩略图缓存

`%LOCALAPPDATA%\Microsoft\Windows\Explorer` 目录下的 `thumbcache_*.db` 文件，可通过 `cleanmgr` 勾选"缩略图"清理，或在文件夹选项中关闭缩略图预览后手动删除。

### 浏览器缓存

各浏览器设置内均有"清除浏览数据"选项，可清除缓存文件、Cookie 等。

以 Chrome 为例：缓存位于 `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache`，也可在浏览器设置 → 隐私和安全 → 清除浏览数据中操作。

### WinSxS 组件存储

`C:\Windows\WinSxS` 是系统组件库，**不要手动删除**，用 DISM 命令清理：

```bat
DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase
```

执行后无法回滚到旧版本的 Windows 更新，但通常能释放数 GB 空间。

### `hiberfil.sys`（休眠文件）

如果不使用休眠功能，可以禁用以删除此文件（通常与内存大小相当）：

```bat
powercfg /hibernate off
```
