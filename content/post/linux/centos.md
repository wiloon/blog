---
title: centos basic
author: "-"
date: 2026-05-07T09:53:01+08:00
url: centos
categories:
  - Linux
tags:
  - linux
  - centos
  - rhel
  - remix
  - AI-assisted
---
## centos basic

## RHEL-based 发行版（CentOS EOL 后）

CentOS 在 2024 年完全 EOL 后，主流的 RHEL 下游发行版：

**免费的 1:1 RHEL 重建版（CentOS 直接替代）：**

- **AlmaLinux** — 社区驱动，由 CloudLinux 公司支持，目前最流行
- **Rocky Linux** — 由 CentOS 原创始人 Gregory Kurtzer 创建，同样非常流行

**商业版：**

- **RHEL**（Red Hat Enterprise Linux）— 上游源，通过 Red Hat 开发者计划可免费用于最多 16 个生产系统
- **Oracle Linux** — Oracle 的重建版，免费使用，付费支持

**其他：**

- **CentOS Stream** — 仍然存在，但现在是下一个 RHEL 版本的*滚动预览*（位于 RHEL 上游而非下游），稳定性不如旧版 CentOS

AlmaLinux 和 Rocky Linux 都提供迁移工具（`almalinux-deploy` / `migrate2rocky`），可将现有 CentOS 系统原地转换。

## AlmaLinux

AlmaLinux 是 CloudLinux 公司主导的 RHEL 下游发行版。

### 升级软件包

**同主版本内更新所有软件包：**

```bash
sudo dnf upgrade
# 加 --refresh 强制刷新缓存
sudo dnf --refresh upgrade
```

`dnf update` 是 `dnf upgrade` 的别名（alias），两者完全等价。与旧版 yum 不同，DNF 统一了这两个命令，推荐使用 `dnf upgrade`。

**跨主版本升级（如 AlmaLinux 8 → 9），使用官方工具 Leapp：**

```bash
sudo dnf install leapp-upgrade
sudo leapp preupgrade   # 预检，生成报告，不实际升级
sudo leapp upgrade      # 执行升级，需要重启
```

`leapp preupgrade` 会列出潜在问题和阻断项（inhibitors），必须先解决才能继续。

```bash
# The containerd.io package contains runc too, but does not contain CNI plugins.
sudo dnf install containerd.io
```

## AlmaLinux 9 升级到 10

### 前置条件

- 确认当前版本是 AlmaLinux 9（`cat /etc/almalinux-release`）
- 确保系统已完全更新到最新的 9.x 补丁版本
- 备份重要数据
- 确保有足够磁盘空间（至少 5GB 可用空间）
- 建议在非生产环境先测试

### 第一步：更新当前系统到最新

```bash
sudo dnf upgrade --refresh -y
sudo reboot
```

### 第二步：安装 Leapp 升级工具

```bash
sudo dnf install -y leapp-upgrade
```

### 第三步：运行预检（preupgrade）

```bash
sudo leapp preupgrade
```

预检完成后查看报告：

```bash
sudo leapp report
# 或查看报告文件
cat /var/log/leapp/leapp-report.txt
```

报告中的条目分为两类：

- **inhibitor**（阻断项）— 必须全部解决，否则无法继续升级
- **warning**（警告）— 建议处理，但不阻断升级

### 第四步：处理阻断项

常见阻断项处理示例：

```bash
# 如果有 SELinux 相关阻断，确保 SELinux 不是 disabled 状态
# /etc/selinux/config 中 SELINUX=enforcing 或 permissive

# 如果有第三方软件源阻断，禁用相关 repo
sudo dnf config-manager --disable <repo-name>

# 确认没有已知不兼容的内核模块
sudo leapp answer --section remove_pam_pkcs11_module_check.confirm=True
```

重复运行 `sudo leapp preupgrade` 直到没有 inhibitor。

### 第五步：执行升级

```bash
sudo leapp upgrade
```

命令执行完成后系统会自动重启，进入升级专用的临时环境完成实际升级过程（这一步耗时较长，约 15~30 分钟）。

### 第六步：升级后验证

重启进入新系统后：

```bash
# 确认版本
cat /etc/almalinux-release

# 检查内核版本
uname -r

# 清理旧的 leapp 相关包和旧内核
sudo dnf remove $(rpm -qa | grep el9) 2>/dev/null
sudo dnf autoremove -y

# 重新启用之前禁用的第三方 repo（按需）
```

---

centos 7 minimal 安装之后 磁盘占用 1.4G

- yum repo

    curl -o /etc/yum.repos.d/CentOS-Base.repo [https://mirrors.aliyun.com/repo/Centos-7.repo](https://mirrors.aliyun.com/repo/Centos-7.repo)

## dhcp

    vim /etc/sysconfig/network-scripts/ifcfg-eth0

    bootproto=dhcp
    onboot=yes

## Linux centos livecd bin netinstall 各版本的区别

CentOS-5.5-x86_64-LiveCD.iso 光盘系统
  
CentOS-5.5-x86_64-bin-DVD 64位安装盘
  
CentOS-5.5-x86_64-netinstall 64位网络安装盘

LiveCD一般用来修复系统使用，有容量很小，不用安装，可以自启动等特性，可以直接使用光盘启动的系统。 bin DVD也具有同样的功能，但是体积较大，需要安装到硬盘使用。 netinstall和bin都可以用来安装系统，不同的是，netinstall根据你选择的软件列表从网上下载，然后进行系统安装； bin DVD本身包含了软件，不需要依赖于网络经行安装。

## centos, rpm

### centos, rpm 查看软件的版本号

rpm -qa | grep mysql

### RHEL/CentOS/Fedora 源 EPEL、Remi、RPMForge、RPMFusion

#### centos7, aliyun mirror

    curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo

[http://www.cnblogs.com/mawanglin2008/p/3532247.html](http://www.cnblogs.com/mawanglin2008/p/3532247.html)

RHEL/CentOS/Fedora各种源(EPEL、Remi、RPMForge、RPMFusion)配置

CentOS默认自带CentOS-Base.repo源,但官方源中去除了很多有版权争议的软件,而且安装的软件也不是最新的稳定版。Fedora自带的源中也找不到很多多媒体软件,如果需要安装,必需先添加其他源,如RPMFusion和RPMForge等第三方软件库。

下面GoFace来一一介绍各种第三方软件库,以下软件库适用于与RHEL完全兼容的linux发行版,如CentOS,Fedora,Scientific Linux。Scientific Linux大家可能有点陌生,它与CentOS类似,是RedHat Linux的克隆版,GoFace之前有过介绍: [http://blog.51osos.com/linux/scientific-linux/](http://blog.51osos.com/linux/scientific-linux/)

### EPEL源

EPEL, 即Extra Packages for Enterprise Linux,是由 Fedora 社区创建维护,为 RHEL 及衍生发行版如 CentOS、Scientific Linux 等提供高质量软件包的项目。EPEL中含有大量的软件,对官方标准源是一个很好的补充。

"EPEL (Extra Packages for Enterprise Linux ) is a Fedora Special Interest Group that creates, maintains, and manages a high quality set of additional packages for Enterprise Linux, including, but not limited to, Red Hat Enterprise Linux (RHEL), CentOS and Scientific Linux (SL)."

wiki:[http://fedoraproject.org/wiki/EPEL](http://fedoraproject.org/wiki/EPEL)

Fedora EPEL 下载: [http://mirrors.fedoraproject.org/publiclist/EPEL/](http://mirrors.fedoraproject.org/publiclist/EPEL/)

EPEL 下载地址: [http://download.fedora.redhat.com/pub/epel/](http://download.fedora.redhat.com/pub/epel/)

请针对不同的版本下载相应的包。

例如CentOS6.5添加阿里云的EPEL源

yum localinstall -nogpgcheck [http://mirrors.aliyun.com/epel/6/x86_64/epel-release-6-8.noarch.rpm](http://mirrors.aliyun.com/epel/6/x86_64/epel-release-6-8.noarch.rpm)
  
CentOS 7.0添加阿里云的EPEL源

yum localinstall -nogpgcheck [http://mirrors.aliyun.com/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm](http://mirrors.aliyun.com/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm)
  
### Remi源
  
Remi源大家或许很少听说,不过Remi源GoFace强烈推荐,尤其对于不想编译最新版的linux使用者,因为Remi源中的软件几乎都是最新稳定版。或许您会怀疑稳定不？放心吧,这些都是Linux骨灰级的玩家编译好放进源里的,他们对于系统环境和软件编译参数的熟悉程度毋庸置疑。

Remi下载地址: [http://rpms.famillecollet.com/](http://rpms.famillecollet.com/)

您也需要针对不同的版本号下载。

例如CentOS 6.5添加官方的Remi源

yum localinstall -nogpgcheck [http://rpms.famillecollet.com/enterprise/remi-release-6.rpm](http://rpms.famillecollet.com/enterprise/remi-release-6.rpm)
  
例如CentOS 7添加官方的Remi源

yum localinstall -nogpgcheck [http://rpms.famillecollet.com/enterprise/remi-release-7.rpm](http://rpms.famillecollet.com/enterprise/remi-release-7.rpm)
  
RPMForge源

RPMForge是CentOS系统下的软件仓库,拥有4000多种的软件包,被CentOS社区认为是最安全也是最稳定的一个软件仓库。

RPMForge官方网站: [http://repoforge.org/](http://repoforge.org/)

RPMForge下载地址:

32位: [http://apt.sw.be/redhat/el6/en/i386/rpmforge/RPMS/](http://apt.sw.be/redhat/el6/en/i386/rpmforge/RPMS/)

64位: [http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/](http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/)

例如CentOS6.5添加官方的RPMForge源

yum localinstall -nogpgcheck [http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm](http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm)
  
CentOS 7.0添加官方的RPMForge源

yum localinstall -nogpgcheck [http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm](http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm)
  
RPMFusion源

如果您现在正在使用Fedora 15,对RPMFusion一定不陌生吧,各种音频软件如MPlayer在标准源中是没有的,一般先安装RPMFusion源,之后就可以放便地yum install各种需要的软件啦。

CentOS官方说RPMFusion软件库里面的软件稳定性不如rpmforge。

RPMFusion官网: [http://rpmfusion.org/](http://rpmfusion.org/)

例如CentOS6.5添加阿里云的RPMFusion源

yum localinstall -nogpgcheck [http://mirrors.aliyun.com/rpmfusion/free/el/updates/6/x86_64/rpmfusion-free-release-6-1.noarch.rpm](http://mirrors.aliyun.com/rpmfusion/free/el/updates/6/x86_64/rpmfusion-free-release-6-1.noarch.rpm)
  
yum localinstall -nogpgcheck [http://mirrors.aliyun.com/rpmfusion/nonfree/el/updates/6/x86_64/rpmfusion-nonfree-release-6-1.noarch.rpm](http://mirrors.aliyun.com/rpmfusion/nonfree/el/updates/6/x86_64/rpmfusion-nonfree-release-6-1.noarch.rpm)
  
或者添加CentOS6.5官方的RPMFusion源

yum localinstall -nogpgcheck [http://download1.rpmfusion.org/free/el/updates/6/i386/rpmfusion-free-release-6-1.noarch.rpm](http://download1.rpmfusion.org/free/el/updates/6/i386/rpmfusion-free-release-6-1.noarch.rpm)
  
yum localinstall -nogpgcheck [http://download1.rpmfusion.org/nonfree/el/updates/6/i386/rpmfusion-nonfree-release-6-1.noarch.rpm](http://download1.rpmfusion.org/nonfree/el/updates/6/i386/rpmfusion-nonfree-release-6-1.noarch.rpm)
  
注意: 在安装RPMFusion源之前需要先安装 epel-release

yum localinstall [http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm](http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm)
  
其他版本请详见: [http://rpmfusion.org/Configuration](http://rpmfusion.org/Configuration)

如何使用各种源
  
以上源对CentOS等系统完全兼容,但各软件库之间并不能保证完全兼容没有冲突。如果您需要使用以上源,您需要安装yum-priorities插件。安装yum-priorities插件后,您可以给各个源设置优先级priority。一般设置官方标准源优先级为1,最高,第三方推荐>10

priority=N  (N为1到99的正整数,数值越小越优先)

[base], [addons], [updates], [extras] … priority=1
  
[CentOSplus],[contrib] … priority=2
  
其他第三的软件源为: priority=N  (推荐N>10)

vi CentOS-Base.repo

[base]

name=CentOS-$releasever - Base

mirrorlist=[http://mirrorlist.centos.org/?release](http://mirrorlist.centos.org/?release)=$releasever&arch=$basearch&repo=os

aseurl=[http://mirror.centos.org/centos/](http://mirror.centos.org/centos/)$releasever/os/$basearch/

gpgcheck=1

gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-6

priority=1

released updates

……

wget [http://download.fedora.redhat.com/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm](http://download.fedora.redhat.com/pub/epel/6/x86_64/epel-release-6-5.noarch.rpm)

wget [http://rpms.famillecollet.com/enterprise/remi-release-6.rpm](http://rpms.famillecollet.com/enterprise/remi-release-6.rpm)

[root@orcl1 yum.repos.d]# ls

CentOS-Base.repo CentOS-Media.repo epel-testing.repo

CentOS-Debuginfo.repo epel.repo remi.repo
  
vi remi.repo 将[remi] 中的 enabled=0 改成 enabled=1 来启用 remi 源

[root@orcl1 yum.repos.d]# rpm –import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

[root@orcl1 yum.repos.d]# rpm –import /etc/pki/rpm-gpg/RPM-GPG-KEY-remi
  
在remi.repo中和epel.repo中添加priority设置即可使用。

## centos 7 repo

https://henchat.net/centos%E7%B3%BB%E7%BB%9F%E8%BF%98%E5%8E%9F%E5%AE%98%E6%96%B9yum%E6%BA%90/

```Bash
sed -e "s|^mirrorlist=|#mirrorlist=|g" \
    -e "s|^#baseurl=http://mirror.centos.org/centos/\$releasever|baseurl=https://vault.centos.org/7.9.2009/|g" \
    -e "s|^#baseurl=http://mirror.centos.org/\$contentdir/\$releasever|baseurl=https://vault.centos.org/7.9.2009/|g" \
    -i.bak \
    /etc/yum.repos.d/CentOS-*.repo

```