---
title: nftables trace
author: "-"
date: 2019-03-30T16:14:02+00:00
url: /?p=14030
categories:
  - Inbox
tags:
  - reprint
---
## nftables trace
nhttps://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing

```bash
nft add rule nat post ip saddr 192.168.60.0/24 meta nftrace set 1 oif wlp3s0 masquerade
nft add rule nat post ip protocol icmp icmp type echo-request meta nftrace set 1 accept
nft insert rule nat post ip protocol icmp icmp type echo-request meta nftrace set 1 accept

nft add rule nat post ip protocol icmp icmp type echo-request meta nftrace set 1 log

nft monitor trace
```