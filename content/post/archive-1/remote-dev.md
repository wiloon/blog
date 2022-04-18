---
title: remote dev
author: "-"
date: 2015-02-05T08:27:05+00:00
url: remote/dev
categories:
  - dev
tags:
  - remix
---
## remote dev

## vm@server, xforward

- 延迟: 22ms
- 内存: 16G+
- cpu: 8c
- 无线网带宽问题，延迟

编辑器内部纵向滚动屏幕带宽占用峰值2300KB/s

## jetbrain remote development

beta 版本 不稳定.

## vm@server, rdp

Ubuntu 22.04 安装 xrdp 开放 3389 端口, win10 mstsc 连接到 3389, 拖动窗口有延迟, 编辑器内部纵向滚动屏幕延迟可以接受. 拖动窗口带宽占用峰值 1700KB/s, 编辑器内部纵向滚动屏幕带宽占用峰值500KB/s

- 延迟: 22ms
- 内存: 16G+
- cpu: 8c

## vm@server, vnc

- 延迟: 22ms
- 内存: 16G+
- cpu: 8c
- 图形界面延迟

基于像素的传输,画质不好.

## wsl + x server

- 延迟: <1ms
- 内存: 16G+
- cpu: 4c
- 内存占用问题

## wsl + idea

- 延迟: <1ms
- 内存: 16G+
- cpu: 4c
- 磁盘性能问题

## windows + idea

- 延迟: <1ms
- 内存: 16G+
- cpu: 4c
- ansible,git,leveldb 问题
