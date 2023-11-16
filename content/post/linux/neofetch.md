---
author: "-"
date: "2021-04-30 17:54:53" 
title: "neofetch, linux logo ascii"
categories:
  - inbox
tags:
  - reprint
---
## "neofetch, linux logo ascii"

## neofetch, linux logo ascii

neofetch 是一个跨平台的易于使用的 系统信息显示命令行脚本，它收集你的系统信息，并在终端中和图像一起显示出来，这个图像可能是你的发行版的 logo 也可能是你选择的一幅 ascii 艺术字。

Neofetch 和 ScreenFetch 或者 Linux_Logo 很像，但是它可以高度定制，并且还有一些额外的我们要在下面讨论的特点。

它的主要特点有: 运行速度快，可以显示全色图像 —— 用 ASCII 字符显示的发行版 logo ，旁边显示系统信息，可以高度定制，可以随时随地显示系统信息，并且在脚本结束的时候还可以通过一个特殊的参数来启用桌面截图。

系统要求:
Bash 3.0+ 带 ncurses 支持。
w3m-img (有时候会打包成 w3m) 或者 iTerm2 或者 Terminology，用于显示图像。
imagemagick，用于创建缩略图。
支持 [\033[14t 的 Linux 终端模拟器 或者 xdotool 或者 xwininfo + xprop 或者 xwininfo + xdpyinfo 。
Linux 系统中还需要 feh、nitrogen 或者 gsettings 来提供对墙纸的支持。
注意: 你可以从 Neofetch 的 Github 页面了解更多关于可选依赖的信息，以检查你的 Linux 终端模拟器 是不是真的支持 \033[14t 或者是否需要一些额外的依赖来使这个脚本在你的发行版上工作得更好。

```bash
                   -`                    wiloon@nuc 
                  .o+`                   ---------- 
                 `ooo/                   OS: Arch Linux x86_64 
                `+oooo:                  Host: NUC8i5BEH J72747-308 
               `+oooooo:                 Kernel: 5.16.1-arch1-1 
               -+oooooo+:                Uptime: 9 days, 13 hours, 20 mins 
             `/:-:++oooo+:               Packages: 764 (pacman) 
            `/++++/+++++++:              Shell: zsh 5.8 
           `/++++++++++++++:             Resolution: 1920x1200, 1920x1200 
          `/+++ooooooooooooo/`           DE: Plasma 5.23.5 
         ./ooosssso++osssssso+`          WM: KWin 
        .oossssso-````/ossssss+`         Theme: Breeze Light [Plasma], Breeze [GTK2/3] 
       -osssssso.      :ssssssso.        Icons: breeze [Plasma], breeze [GTK2/3] 
      :osssssss/        osssso+++.       Terminal: konsole 
     /ossssssss/        +ssssooo/-       CPU: Intel i5-8259U (8) @ 3.800GHz 
   `/ossssso+/:-        -:/+osssso+-     GPU: Intel CoffeeLake-U GT3e [Iris Plus Graphics 655] 
  `+sso+:-`                 `.-/+oso:    Memory: 10730MiB / 15870MiB 
 `++:.                           `-/+/
 .`                                 `/                           
                                                                 
```

---

[https://linux.cn/article-8013-1.html](https://linux.cn/article-8013-1.html)
