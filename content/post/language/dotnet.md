---
title: dotnet
author: "-"
date: 2014-11-29T14:33:14+00:00
url: dotnet
categories:
  - dotnet
tags:
  - reprint
  - remix
---
## dotnet

dotnet-sdk-8.0 (开发工具)
├── dotnet-runtime-8.0 (运行时)
├── dotnet-targeting-pack-8.0 (编译支持)
├── dotnet-templates-8.0 (模板)
├── dotnet-apphost-pack-8.0 (发布支持)
└── dotnet-host-8.0 (主机)
    └── dotnet-hostfxr-8.0 (解析器)

```bash
# 1. 下载并安装Microsoft GPG密钥和仓库配置
wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
# wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb

# 2. 更新包列表
sudo apt update

# 3. 安装.NET 7.0 SDK
sudo apt install dotnet-sdk-7.0
### -------------------------------


sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get install -y dotnet-sdk-7.0

sudo apt-get update && sudo apt-get install -y apt-transport-https
dotnet --version
dotnet --info
apt-cache policy dotnet-sdk-8.0
sudo apt install dotnet-sdk-7.0 -y
dotnet --list-runtimes
dotnet build --verbosity minimal
dotnet run --dry-run

```
