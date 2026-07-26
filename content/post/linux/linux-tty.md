---
title: "Linux TTY 与伪终端 PTY"
author: "-"
date: 2014-08-11T12:06:08+00:00
lastmod: 2026-07-26T13:50:51+08:00
url: linux-tty
categories:
  - Linux
tags:
  - Linux
  - tty
  - pty
  - remix
  - AI-assisted
aliases:
  - /p5002/
  - /p5335/
  - /p5544/
  - /p5645/
  - /p6302/
  - /p6932/
  - /p7609/
  - /p8204/
---

## TTY 是什么

tty 一词源自 teletype（电传打字机）：通过串行线，键盘输入和打印机输出来回传递信息的设备，现在这个词泛指所有类型的终端设备。终端是一种字符型设备。

在支持多任务的计算机出现之前，两台 teletype 直接用物理线路相连：

```text
+----------+     Physical Line     +----------+
| teletype |<--------------------->| teletype |
+----------+                       +----------+
```

计算机支持多任务之后，人们把这些 teletype 接到计算机上当终端用（一是当时已有大量现成的 teletype 设备，二是相关网络已经比较成熟），连接方式变成：

```text
                                                                      +----------+
+----------+   +-------+     Physical Line     +-------+   +------+   |          |
| Terminal |<->| Modem |<--------------------->| Modem |<->| UART |<->| Computer |
+----------+   +-------+                       +-------+   +------+   |          |
                                                                      +----------+
```

左边的 Terminal 就是各种 teletype；物理线路两端接的 Modem 就是我们常说的"猫"；UART 负责把 teletype 的信号转换成计算机能识别的信号。

## /dev 下的几类终端设备文件

| 类型 | 设备文件 | 说明 |
| ---- | ---- | ---- |
| 串行端口终端 | `/dev/ttySn`（如 `/dev/ttyS0`） | 通过计算机串口连接的终端，对应 DOS 下的 COM1、COM2 等；`echo test > /dev/ttyS1` 可以把 `test` 发送到接在该端口上的设备 |
| 伪终端 | `/dev/pty/`（成对出现，如 `ptyp3`/`ttyp3`） | 一对逻辑终端设备，不直接对应物理硬件；一端读写会反映到另一端，类似管道；`ttyp3` 供普通程序当串口用，`ptyp3` 需要专门设计的程序（如 telnet、getty）使用 |
| 控制终端 | `/dev/tty` | 当前进程的控制终端；`ps -ax` 可查看进程关联的控制终端，`tty` 命令可查看具体对应哪个实际设备 |
| 控制台终端 | `/dev/ttyn`、`/dev/console` | UNIX 里显示器通常称为控制台；`tty1`-`tty6` 是虚拟终端，`Alt+F1`~`F6` 切换，`tty0` 是当前虚拟终端的别名，系统信息统一发到这里 |
| 其它 | 例如 `/dev/ttyIn` | 针对 ISDN 等具体设备的终端特殊文件 |

## pty：伪终端

如果是远程 telnet 到主机，或者用 xterm，并没有物理终端，这时候就要靠伪终端 **pty（pseudo-tty）**。

pty 由一对设备构成：**ptmx**（pseudo-terminal master）和 **pts**（pseudo-terminal slave，`/dev/pts/N`）配合实现。进程通过调用 API（如 `posix_openpt()`）向 ptmx 请求创建一个 pts，会得到连接到 ptmx 的读写 fd，以及一个新创建的 pts；ptmx 内部维护这个 fd 和 pts 的对应关系，之后往这个 fd 的读写会被 ptmx 转发到对应的 pts。

打开一个终端窗口就会得到一个新的 `pts/N`（再打开一个就是 `pts/N+1`）。

## 内核 TTY 子系统

```text
    +-----------------------------------------------+
    |                    Kernel                     |
    |                                 +--------+    |
    |   +--------+   +------------+   |        |    |       +----------------+
    |   |  UART  |   |    Line    |   |  TTY   |<---------->| User process A |
<------>|        |<->|            |<->|        |    |       +----------------+
    |   | driver |   | discipline |   | driver |<---------->| User process B |
    |   +--------+   +------------+   |        |    |       +----------------+
    |                                 +--------+    |
    |                                               |
    +-----------------------------------------------+
```

- **UART driver**：对接外部 UART 硬件
- **Line discipline**：对输入输出做处理，可以看作 TTY driver 的一部分
- **TTY driver**：处理各种终端设备，用户空间进程通过它和终端打交道

对每一个连接进来的终端，TTY driver 都会创建一个对应的 TTY 设备：

```text
                      +----------------+
                      |   TTY Driver   |
                      |                |
                      |   +-------+    |       +----------------+
 +------------+       |   |       |<---------->| User process A |
 | Terminal A |<--------->| ttyS0 |    |       +----------------+
 +------------+       |   |       |<---------->| User process B |
                      |   +-------+    |       +----------------+
                      |                |
                      |   +-------+    |       +----------------+
 +------------+       |   |       |<---------->| User process C |
 | Terminal B |<--------->| ttyS1 |    |       +----------------+
 +------------+       |   |       |<---------->| User process D |
                      |   +-------+    |       +----------------+
                      |                |
                      +----------------+
```

驱动收到终端连接时，会根据型号和参数创建相应的 tty 设备（图中叫 `ttyS0` 是因为大部分终端走串行连接）；每个终端按键习惯可能不同（比如 delete 键是删前面还是删后面），所以每个 tty 设备的配置可能都不一样，这也是终端模拟器默认配置和使用习惯不符时需要做个性化配置的原因。

随着计算机发展，teletype 逐渐消失，每台机器都有自己的键盘和显示器，远程操作改用 SSH 实现，但内核的 TTY 驱动架构没变——想和系统里的进程做 I/O 交互，还是要通过 TTY 设备，于是出现了各种终端模拟软件，模拟的也是常见的几种终端类型，如 VT100、VT220、XTerm 等。

## 常用命令

```bash
# check which tty the current shell is attached to
tty

# check which processes have this tty open
lsof /dev/pts/1

# writing to a tty directly has the same effect as writing to stdout
echo foo > /dev/pts/1

# write red text to another pts (ANSI escape code)
echo -e "\033[31mFoo\033[0m" > /dev/pts/2

# list all terminal types supported by the system
toe -a

# compare two terminal types
infocmp vt100 vt220
```

示例输出：

```text
$ tty
/dev/pts/1

$ lsof /dev/pts/1
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
bash     907  dev    0u   CHR  136,1      0t0    4 /dev/pts/1
bash     907  dev    1u   CHR  136,1      0t0    4 /dev/pts/1
bash     907  dev    2u   CHR  136,1      0t0    4 /dev/pts/1
bash     907  dev  255u   CHR  136,1      0t0    4 /dev/pts/1
lsof    1118  dev    0u   CHR  136,1      0t0    4 /dev/pts/1
lsof    1118  dev    1u   CHR  136,1      0t0    4 /dev/pts/1
lsof    1118  dev    2u   CHR  136,1      0t0    4 /dev/pts/1
```

从输出可以看出，`bash` 和 `lsof` 进程的 stdin(0u)、stdout(1u)、stderr(2u) 都绑定到了同一个 TTY 上，pts 本身也是一种 tty 设备。

## tty 与进程、I/O 设备的关系

可以把 tty 理解成一个管道（pipe）：一端写的内容可以从另一端读出来，反之亦然。

```text
    Input       +--------------------------+    R/W     +------+
    ----------->|                          |<---------->| bash |
                |          pts/1           |            +------+
    <-----------|                          |<---------->| lsof |
    Output      | Foreground process group |    R/W     +------+
                +--------------------------+
```

`input`/`output` 可以简单理解成键盘和显示器。tty 里有一个重要属性叫 **Foreground process group**，记录当前前台的进程组是哪一个：

- pts/1 收到 input 的输入后，会检查当前前台进程组，把输入放进该进程组 leader 的输入缓存，leader 进程就能通过 `read` 拿到用户输入
- 前台进程组里的进程往 tty 写数据时，tty 会把数据输出到 output 设备
- 在 shell 里执行不同命令时，前台进程组会不断变化，这个变化由 shell 负责更新到 tty 设备

由此可知，后台进程只要不读写 tty 就不会有问题——写后台程序（daemon）时，需要把 stdin/stdout/stderr 重定向到别处。非前台进程组读写 tty 会怎样，见下文「TTY 相关信号」里的 `SIGTTIN`/`SIGTTOU`。

## TTY 是如何被创建的

### 键盘显示器直连（物理终端）

```text
                   +-----------------------------------------+
                   |          Kernel                         |
                   |                           +--------+    |       +----------------+
 +----------+      |   +-------------------+   |  tty1  |<---------->| User processes |
 | Keyboard |--------->|                   |   +--------+    |       +----------------+
 +----------+      |   | Terminal Emulator |<->|  tty2  |<---------->| User processes |
 | Monitor  |<---------|                   |   +--------+    |       +----------------+
 +----------+      |   +-------------------+   |  tty3  |<---------->| User processes |
                   |                           +--------+    |       +----------------+
                   |                                         |
                   +-----------------------------------------+
```

键盘、显示器都和内核里的终端模拟器相连，由模拟器决定创建多少个 tty。比如按 `Ctrl+Alt+F1` 时，模拟器捕获该输入并激活 `tty1`，键盘输入转发给 `tty1`，`tty1` 的输出转发给显示器；`Ctrl+Alt+F2` 则切到 `tty2`。

模拟器激活某个 tty 时，如果发现还没有进程与之关联（第一次打开），就会启动配置好的进程并绑定，通常是负责登录的进程。切换到 `tty2` 后，`tty1` 的输出仍然发给模拟器，模拟器为每个 tty 维护一份缓存，但缓存空间有限，切回 `tty1` 时只能看到最近的输出。

### SSH 远程访问

```text
 +----------+       +------------+
 | Keyboard |------>|            |
 +----------+       |  Terminal  |
 | Monitor  |<------|            |
 +----------+       +------------+
                          |
                          |  ssh protocol
                          |
                          ↓
                    +------------+
                    |            |
                    | ssh server |--------------------------+
                    |            |           fork           |
                    +------------+                          |
                        |   ↑                               |
                        |   |                               |
                  write |   | read                          |
                        |   |                               |
                  +-----|---|-------------------+           |
                  |     |   |                   |           ↓
                  |     ↓   |      +-------+    |       +-------+
                  |   +--------+   | pts/0 |<---------->| shell |
                  |   |        |   +-------+    |       +-------+
                  |   |  ptmx  |<->| pts/1 |<---------->| shell |
                  |   |        |   +-------+    |       +-------+
                  |   +--------+   | pts/2 |<---------->| shell |
                  |                +-------+    |       +-------+
                  |    Kernel                   |
                  +-----------------------------+
```

这里的 Terminal 可以是任意客户端（比如 Windows 上的 PuTTY），它需要实现 SSH 客户端功能；下面用 sshd 代替 SSH 服务器程序，分建立连接和收发数据两条线来看。

**建立连接**

1. Terminal 请求和 sshd 建立连接
2. 验证通过后，sshd 创建一个新的 session
3. sshd 调用 `posix_openpt()` 请求 ptmx 创建一个 pts，得到和 ptmx 关联的 fd，并把该 fd 与 session 关联起来
4. sshd 创建 shell 进程，将新创建的 pts 和 shell 绑定

pty（pseudo terminal device）由两部分构成：ptmx 是 master 端，pts 是 slave 端。此时可以看到 sshd 已经打开了 `/dev/ptmx`：

```text
$ sudo lsof /dev/ptmx
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1191  dev    8u   CHR    5,2      0t0 6531 /dev/ptmx
sshd    1191  dev   10u   CHR    5,2      0t0 6531 /dev/ptmx
sshd    1191  dev   11u   CHR    5,2      0t0 6531 /dev/ptmx
```

**收发消息**

1. Terminal 收到键盘输入，通过 SSH 协议发给 sshd
2. sshd 根据自己管理的 session，找到该客户端对应、关联到 ptmx 上的 fd
3. 往这个 fd 写入客户端发来的数据
4. ptmx 收到数据后，根据 fd 找到对应的 pts（对应关系由 ptmx 自动维护），把数据包转发给该 pts
5. pts 收到数据包后，检查绑定到自己的当前前台进程组，把数据发给该进程组的 leader
6. pts 上只有 shell，所以 shell 的 `read` 就收到了这个数据包
7. shell 处理收到的数据包，输出处理结果（也可能没有输出）
8. shell 通过 `write` 把结果写入 pts
9. pts 把结果转发给 ptmx
10. ptmx 根据 pts 找到对应的 fd，把结果写入该 fd
11. sshd 收到该 fd 的结果后，找到对应的 session，把结果发给对应的客户端

### 键盘显示器直连（图形界面）

结构和 SSH 场景类似，区别是这里的 Terminal（终端模拟器）不需要实现 SSH 客户端，但要把 SSH 服务器要干的活也干了（通信协议部分除外）：

```text
 +----------+       +------------+
 | Keyboard |------>|            |
 +----------+       |  Terminal  |--------------------------+
 | Monitor  |<------|            |           fork           |
 +----------+       +------------+                          |
                        |   ↑                               |
                        |   |                               |
                  write |   | read                          |
                        |   |                               |
                  +-----|---|-------------------+           |
                  |     |   |                   |           ↓
                  |     ↓   |      +-------+    |       +-------+
                  |   +--------+   | pts/0 |<---------->| shell |
                  |   |        |   +-------+    |       +-------+
                  |   |  ptmx  |<->| pts/1 |<---------->| shell |
                  |   |        |   +-------+    |       +-------+
                  |   +--------+   | pts/2 |<---------->| shell |
                  |                +-------+    |       +-------+
                  |    Kernel                   |
                  +-----------------------------+
```

### SSH + Screen/Tmux

用 screen/tmux 启动的进程，即使网络断开也不受影响，下次连上还能看到之前的所有输出，接着干活。以 tmux 为例：

```text
 +----------+       +------------+
 | Keyboard |------>|            |
 +----------+       |  Terminal  |
 | Monitor  |<------|            |
 +----------+       +------------+
                          |
                          |  ssh protocol
                          |
                          ↓
                    +------------+
                    |            |
                    | ssh server |--------------------------+
                    |            |           fork           |
                    +------------+                          |
                        |   ↑                               |
                        |   |                               |
                  write |   | read                          |
                        |   |                               |
                  +-----|---|-------------------+           |
                  |     ↓   |                   |           ↓
                  |   +--------+   +-------+    |       +-------+  fork   +-------------+
                  |   |  ptmx  |<->| pts/0 |<---------->| shell |-------->| tmux client |
                  |   +--------+   +-------+    |       +-------+         +-------------+
                  |   |        |                |                               ↑
                  |   +--------+   +-------+    |       +-------+               |
                  |   |  ptmx  |<->| pts/2 |<---------->| shell |               |
                  |   +--------+   +-------+    |       +-------+               |
                  |     ↑   |  Kernel           |           ↑                   |
                  +-----|---|-------------------+           |                   |
                        |   |                               |                   |
                        |w/r|   +---------------------------+                   |
                        |   |   |            fork                               |
                        |   ↓   |                                               |
                    +-------------+                                             |
                    |             |                                             |
                    | tmux server |<--------------------------------------------+
                    |             |
                    +-------------+
```

系统里的 ptmx 只有一个，图中画了两个是为了表示 tmux 服务器和 sshd 都用 ptmx，但彼此互不干涉。

流程前半段和普通 SSH 一样，区别是 `pts/0` 关联的前台进程不是 shell，而是 tmux 客户端——SSH 客户端发来的数据包会被 tmux 客户端收到，再转发给 tmux 服务器；tmux 服务器的活和 sshd 类似，维护一堆 session，为每个 session 创建一个 pts，把 tmux 客户端发来的数据转发给对应的 pts。

由于 tmux 服务器只和 tmux 客户端打交道、跟 sshd 没关系，终端和 sshd 的连接断开时，虽然 `pts/0` 会被关闭，相关的 shell 和 tmux 客户端也会被 kill，但不影响 tmux 服务器；下次用 tmux 客户端连上 tmux 服务器，看到的还是上次的内容。

## TTY 和 PTS 的区别

对用户空间的程序来说，两者没有区别。从内核角度看：

- pts 的另一端连接的是 ptmx
- tty 的另一端连接的是内核的终端模拟器

ptmx 和终端模拟器都只负责维护会话和转发数据包；再往后看，ptmx 的另一端连接的是用户空间应用程序（如 sshd、tmux），而内核终端模拟器的另一端连接的是具体硬件（键盘、显示器）。

## 常见 TTY 配置

```text
$ stty -a
speed 38400 baud; rows 51; columns 204; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = M-^?; eol2 = M-^?; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R; werase = ^W; lnext = ^V; discard = ^O; min = 1; time = 0;
-parenb -parodd -cmspar cs8 -hupcl -cstopb cread -clocal -crtscts
-ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr icrnl ixon -ixoff -iuclc ixany imaxbel -iutf8
opost -olcuc -ocrnl onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0
isig icanon iexten echo echoe echok -echonl -noflsh -xcase -tostop -echoprt echoctl echoke -flusho -extproc
```

`stty` 可以用来修改 tty 参数，具体见 `man stty`。只要是有权限的程序，都可以通过 Linux 提供的 API 修改 TTY 配置：

| 配置项 | 说明 |
| ---- | ---- |
| `rows`/`columns` | 一般由终端控制，窗口大小变化时需要相应机制同步；比如 SSH 协议里有修改窗口大小的参数，sshd 收到客户端请求后通过 API 修改 tty 的这个参数，再由 tty 通过 `SIGWINCH` 信号通知前台程序（shell、vim 等），前台程序收到后重新读取该参数，调整输出排版 |
| `intr = ^C` | 终端输入组合键到控制命令的映射，比如 `Ctrl+C` 不会被转发给前台进程，而是被 tty 转换成 `SIGINT` 信号发送；可以配置成其它组合键，比如 `intr = ^E` |
| `start = ^Q` / `stop = ^S` | 历史遗留的流量控制：`Ctrl+S` 会让 tty 暂停、阻塞所有读写，`Ctrl+Q` 恢复。常见场景是用 `tail -f` 监控日志时按 `Ctrl+S` 暂停刷新、看完再按 `Ctrl+Q` 继续 |
| `echo` | 终端输入字符能立刻看到，是因为 tty 收到字符后会先原样回显一份再交给前台进程处理；`-echo` 表示关闭该功能 |
| `-tostop` | 控制后台进程（如 `./myapp &`）写 tty 时是否输出到终端：`-tostop` 表示会输出；配置为 `tostop` 则不输出，并且 tty 会给该进程发送 `SIGTTOU`，默认行为是暂停该进程 |

## TTY 相关信号

| 信号 | 触发时机 | 默认行为 |
| ---- | ---- | ---- |
| `SIGINT` | 终端输入 `Ctrl+C` | 终止前台进程 |
| `SIGTSTP` | 终端输入 `Ctrl+Z` | 把前台进程组放到后台，暂停组内所有进程 |
| `SIGTTIN` | 后台进程读 tty | 暂停该进程组的执行 |
| `SIGTTOU` | 后台进程写 tty 且配置了 `tostop` | 暂停该进程组的执行 |
| `SIGWINCH` | tty 窗口大小变化 | 通知前台进程重新读取 `rows`/`columns` |
| `SIGHUP` | tty 另一端挂掉（如 SSH session 断开，sshd 关闭了关联 ptmx 的 fd） | 相关进程收到后默认退出 |

这些信号都可以被捕获，修改默认行为。

## 参考来源

- [http://7056824.blog.51cto.com/69854/276610](http://7056824.blog.51cto.com/69854/276610)
- [https://www.zhihu.com/question/21711307](https://www.zhihu.com/question/21711307)
- [http://ytliu.info/blog/2013/09/28/ttyde-na-xie-shi-er/](http://ytliu.info/blog/2013/09/28/ttyde-na-xie-shi-er/)
- [https://segmentfault.com/a/1190000009082089](https://segmentfault.com/a/1190000009082089)
- [https://www.cnblogs.com/sparkdev/p/11460821.html](https://www.cnblogs.com/sparkdev/p/11460821.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-26 | 全文重新分节整理；删除 TTY 历史、`tty`/`lsof`/`echo` 示例、进程与 I/O 结构图、`toe -a`/`infocmp` 提及等大段重复内容（原文近乎完整地出现了两遍）；`/dev` 终端设备文件类型改为表格；TTY 相关信号从散落各处的段落合并为一张表；补充 `lastmod`，categories 由 `inbox` 改为 `Linux`，标签加 `tty`、`pty`、`remix`、`AI-assisted` | 原文档由两份来源拼接而成，大量内容重复两遍，标题层级混乱（部分小标题不是 Markdown 标题），阅读体验差 |
