---
title: font, 字体
author: "-"
date: 2026-01-16T15:30:00+08:00
url: font

categories:
  - inbox
tags:
  - reprint
  - remix
  - AI-assisted
---
## font, 字体

## 主流编程字体

### 等宽编程字体特性

编程字体需要具备以下特点：

- **等宽设计**：每个字符宽度相同，便于代码对齐
- **字符区分度高**：容易区分 `0O`（数字零和字母O）、`1lI`（数字一、小写L和大写I）等相似字符
- **连字支持**（可选）：将 `->`, `=>`, `!=` 等组合显示为单个符号
- **编程符号优化**：清晰的括号、引号、运算符显示
- **舒适的行高和字间距**：长时间编码不易疲劳

### 开源免费字体

#### Cascadia Code

- **开发者**：Microsoft
- **特点**：Windows Terminal 默认字体，支持连字（Cascadia Code PL 变体），包含 Powerline 字形
- **适用场景**：Windows 开发、终端、VS Code
- **安装**：`sudo apt install fonts-cascadia-code` (Ubuntu/Debian)
- **官网**：https://github.com/microsoft/cascadia-code

#### JetBrains Mono

- **开发者**：JetBrains
- **特点**：专为开发者设计，字符高度区分，支持连字，行高适中
- **适用场景**：IntelliJ IDEA、PyCharm 等 JetBrains IDE 推荐
- **官网**：https://www.jetbrains.com/lp/mono/

#### Fira Code

- **开发者**：Mozilla（基于 Fira Sans 和 Fira Mono）
- **特点**：最流行的连字编程字体之一，支持 100+ 连字组合
- **适用场景**：喜欢连字效果的开发者
- **安装**：`sudo apt install fonts-firacode`
- **官网**：https://github.com/tonsky/FiraCode

#### Hack

- **特点**：基于 Bitstream Vera 和 DejaVu，字符区分度极高
- **适用场景**：注重代码可读性，不需要连字
- **安装**：`sudo apt install fonts-hack`
- **官网**：https://sourcefoundry.org/hack/

#### Source Code Pro

- **开发者**：Adobe
- **特点**：优雅的设计，6 种字重，清晰的字符
- **适用场景**：喜欢 Adobe 设计风格
- **安装**：`sudo pacman -S adobe-source-code-pro-fonts` (Arch)
- **官网**：https://adobe-fonts.github.io/source-code-pro/

#### DejaVu Sans Mono

- **特点**：基于 Vera Sans Mono，Unicode 覆盖广
- **适用场景**：多语言编程，Linux 默认等宽字体
- **安装**：大多数 Linux 发行版预装

#### Ubuntu Mono

- **开发者**：Canonical
- **特点**：Ubuntu 系统默认等宽字体，字符清晰
- **适用场景**：Ubuntu 用户

#### Inconsolata

- **开发者**：Raph Levien
- **特点**：简洁紧凑，适合小屏幕
- **适用场景**：小尺寸显示
- **官网**：https://levien.com/type/myfonts/inconsolata.html

#### IBM Plex Mono

- **开发者**：IBM
- **特点**：现代设计，IBM 企业级品质
- **适用场景**：喜欢 IBM 设计语言
- **官网**：https://www.ibm.com/plex/

#### Iosevka

- **特点**：窄字符设计，同屏显示更多代码
- **适用场景**：喜欢紧凑布局，小屏幕
- **官网**：https://typeof.net/Iosevka/

### 商业付费字体

#### SF Mono

- **开发者**：Apple
- **特点**：macOS 和 Xcode 默认等宽字体
- **适用场景**：macOS 开发者
- **获取**：随 macOS 系统或 Xcode 提供

#### Operator Mono

- **开发者**：Hoefler & Co.
- **特点**：优雅的意大利斜体，价格较贵（$199+）
- **适用场景**：追求极致美观
- **官网**：https://www.typography.com/fonts/operator/

#### MonoLisa

- **特点**：专注可读性和长时间编码舒适度
- **价格**：€139 起
- **官网**：https://www.monolisa.dev/

### Nerd Fonts 系列

Nerd Fonts 是在流行编程字体基础上打补丁，添加大量图标字形（Font Awesome、Devicons、Octicons 等）。

- **安装示例**：`yay -S nerd-fonts-jetbrains-mono`（Arch AUR）
- **包含字体**：几乎所有流行编程字体的 Nerd Fonts 版本
- **适用场景**：终端、Vim/Neovim 的 Powerline、图标显示
- **官网**：https://www.nerdfonts.com/

常见 Nerd Fonts 变体：
- JetBrains Mono Nerd Font
- FiraCode Nerd Font
- Hack Nerd Font
- Meslo Nerd Font
- Droid Sans Mono Nerd Font

### 字体选择建议

| 使用场景 | 推荐字体 |
|---------|--------|
| **喜欢连字** | Fira Code, Cascadia Code, JetBrains Mono |
| **不要连字，注重清晰** | Hack, Source Code Pro, DejaVu Sans Mono |
| **终端 + Powerline** | Cascadia Code PL, JetBrains Mono NF, 任意 Nerd Fonts |
| **小屏幕/紧凑布局** | Iosevka, Inconsolata |
| **macOS 原生** | SF Mono |
| **Windows 原生** | Cascadia Code, Consolas |
| **追求美观，预算充足** | Operator Mono, MonoLisa |
| **多语言支持** | DejaVu Sans Mono, Noto Sans Mono |

### yay -S nerd-fonts-droid-sans-mono

### Source Code Pro

sudo pacman -S adobe-source-code-pro-fonts

### Verdana

Verdana，一套非常受欢迎无衬线字体 (Sans Serif) ，由于它在小字上仍有结构清晰端整、阅读辨识容易等高品质的表现，因而在1996年推出后即迅速成为许多领域所爱用的标准字型之一。

此字体的设计源起于微软字型设计小组的维吉尼亚·惠烈 (Virginia Howlett) 希望设计一套具有高办识性、易读性的新字型以供萤幕显示之用，于是她邀请了世界顶级字型设计师之一的马修·卡特 (Matthew Carter) 操刀，以Frutiger字体及爱德华·约翰斯顿 (Edward Johnston) 为伦敦地铁所设计的字体为蓝本，并由Monotype公司的字型微调 (Hint) 专家汤姆·瑞克纳 (Tom Rickner) 担任手工微调。

"Verdana"一名是由"Verdant"和"Ana"两字所组成的。"Verdant"意为"苍翠"，象征著"翡翠之城"西雅图及有"常青州"之称的华盛顿州，"Ana"则来自于维吉尼亚·惠烈大女儿的名字。

### google font

[http://www.googlefonts.cn/](http://www.googlefonts.cn/)

### Calibri

Calibri，一种无衬线字体，为微软Microsoft Office 2007套装软件的默认字体，取代先前Microsoft Word的默认字体Times New Roman以及PowerPoint、Excel和Outlook的默认字体Arial。
  
Calibri是发布于微软Windows Vista六种西方ClearType字体的其中一种，是Microsoft Word默认字体的第一个无衬线字体，先前则是使用Times New Roman为默认字体。
  
Calibri为字型设计师Lucas de Groot替微软开发的字型，曾于2005年字型设计竞赛 (Type Design Competition) 中获得系统字型 (Type System) 类的奖项。其也包含了拉丁文、希腊文以及斯拉夫语的字母。
  
在某个由Wichita州立大学执行的研究中，Calibri是电子邮件、即时通和PowerPoint简报中最常被使用的字体，同时其用于网页设计的排名也相当高。

## font wqy

font-family: 'WenQuanYi Micro Hei';

## 微软雅黑

微软雅黑是美国微软公司委托中国方正集团设计的一款全面支持ClearType技术的字体。蒙纳公司 (Monotype Corporation) 负责了字体的修饰 (Hinting) 工作。它属于OpenType类型，文件名是MSYH.TTF，在字体设计上属于无衬线字体和黑体。
  
该字体家族还包括"微软雅黑Bold" (粗体) ，文件名为MSYHBD.TTF。这个粗体不是单纯的将普通字符加粗，而是在具体笔画上分别进行处理，因此是独立的一个字体。
  
微软雅黑是随着简体中文版Windows Vista一起发布的字体，也是Windows Vista和Windows 7默认的字体。在使用ClearType功能的液晶显示器中，微软雅黑比以前Windows XP默认的中易宋体更加的清晰易读。另外，Microsoft Office 2007简体中文版也附带这个字体。2008年5月6日，微软发布了个用于Windows XP的雅黑字体版本.
  
在涵盖的字库上，微软雅黑支持GBK字符集，包含了Unicode的所有 20902个中文字符以及中国国家标准化组织添加的大约 80个中文字符，还包含了Big5的繁体中文字符和GB2312中的简体中文字符。
  
当使用于不能显示中文字型名称的系统和繁体中文的系统时，会显示为Microsoft YaHei.
