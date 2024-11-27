---
title: 监控一个 APP 的 HTTPS 流量
author: "-"
date: 2020-04-03T02:02:29+00:00
url: app-network
categories:
  - network
tags:
  - reprint
  - remix
---
## 监控一个 APP 的 HTTPS 流量

在家里的电视上安装了 Plex 但是因为众所周知的原因, 
登录 Plex 账号的过程或者登录之后的网络请求遇到了些问题, 
路由器上配置的透明代理配置文件有可能并没有考虑 Plex 常用的地址, 
所以需要用一些工具来分析 Plex 发出了哪些网络请求.

https://www.anquanke.com/post/id/86238

https://calebfenton.github.io/2017/05/27/monitoring-https-of-a-single-app-on-osx/

## 拦截 HTTPS 流量

1. 生成一个根证书
2. 安装这个根证书
3. 用 proxychains 去代理指定的 app
4. 使用 mitmproxy 去拦截流量

## 安装并配置 proxychains

```Bash
# macOS
brew install proxychains-ng
```

创建一个配置文件

```Bash
# macos
/Users/wiloon/.proxychains/proxychains.conf
```

然后加入以下内容

```Bash
strict_chain
quiet_mode
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
http 127.0.0.1 8080
```

strict_chain: 按照列表中出现的代理服务器的先后顺序组成一条链，要求所有的代理服务器都是有效的
quiet_mode: Quiet mode (no output from library)
proxy_dns: Proxy DNS requests - no leak for DNS data
remote_dns_subnet: 设置内部 dns 解析地址返回 IP 的网段
ProxyList: 代理服务器列表

```Bash
# set the class A subnet number to use for the internal remote DNS mapping
# we use the reserved 224.x.x.x range by default,
# if the proxified app does a DNS request, we will return an IP from that range.
# on further accesses to this ip we will send the saved DNS name to the proxy.
# in case some control-freak app checks the returned ip, and denies to
# connect, you can use another subnet, e.g. 10.x.x.x or 127.x.x.x.
# of course you should make sure that the proxified app does not need
# *real* access to this subnet.
# i.e. dont use the same subnet then in the localnet section
# 设置内部 DNS 解析的时候使用的 A 类网段,
# 我们默认使用保留的 224.x.x.x 网段
# 如果被代理的应用发了一个 DNS 请求，我们将从该网段返回一个 IP。
# 被代理应用进一步访问这个 IP 的时候，我们将把缓存的 DNS 名称发给代理服务器。
# 如果一些控制狂的应用程序检查返回的 IP，并拒绝
# 连接，你可以使用另一个子网，例如 10.x.x.x 或 127.x.x.x。
# 当然，你应该确保被代理的应用程序不需要
# 真正访问这个子网。
# 也就是说，不要在 localnet 部分使用相同的子网。
#remote_dns_subnet 127
#remote_dns_subnet 10
remote_dns_subnet 224
```

https://eonun.com/%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/Hacker/proxychains.conf%E8%AF%A6%E8%A7%A3/

## mitmproxy

```Bash
# install mitmproxy
# macOS
brew install mitmproxy
```

给系统安装根证书，默认情况下 mitmproxy 会自动生成一个根证书 `mitmproxy-ca-cert.pem`，
这个根证书位于 `~/.mitmproxy` 目录

```Bash
# 用 finder 打开目录
open ~/.mitmproxy
```

然后打开 Keychain Access，按下组合键 Command + Space ，然后输入 Keychain Access， 回车

双击 mitmproxy 生成的根证书, 在弹出的添加证书的提示窗口中选择 system.

在 keychain access 里能看 mitmproxy 已经被加入 keychain access,  但是图标上有个红叉. 表示系统不信任这个根证书

右键单击, 选择  get info  展开 trust 把 when using this certificate 改成  always trust.

关闭窗口, 会提示输入密码, 然后红叉会消失, 说明系统已经信任这个证书

```Bash
# 或者执行这个命令让系统信任这个证书, 关窗口人时候输入密码和执行这个命令之后输入密码都能让系统信任这个证书
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem
```

运行 mitmproxy

```Bash
# run mitmproxy
# 默认监听 *:8080
mitmproxy
```

测试一下

```Bash
proxychains4 -f /Users/wiloon/.proxychains/proxychains.conf ./curl https://calebfenton.github.io/
proxychains4 -f /Users/wiloon/.proxychains/proxychains.conf wget https://calebfenton.github.io/
proxychains4 curl http://ifconfig.co/
proxychains4 curl https://calebfenton.github.io/
proxychains4 -f /path/to/proxychains.conf curl https://calebfenton.github.io/
```
