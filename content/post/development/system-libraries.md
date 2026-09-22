---
title: "System Libraries: 跨平台底层库速查"
author: "-"
date: 2026-09-22T08:43:14+08:00
lastmod: 2026-09-22T08:43:14+08:00
url: system-libraries
categories:
  - development
tags:
  - library
  - brew
  - linux
  - macOS
  - remix
  - AI-assisted
---

包管理器升级时，经常会看到一些不认识的底层库（`harfbuzz`、`giflib`、`little-cms2` 等）。它们通常不是自己主动装的，而是被某个上层软件依赖，顺带装上。

这篇文章记录这些底层库是什么、做什么、各平台叫什么包名。库本身是跨平台的，macOS（Homebrew）、Linux（apt / pacman / dnf）上都有，因此不按平台拆分。

遇到不认识的包时，怎么在 macOS 上查依赖关系，见 [Homebrew (brew)](../macos/brew.md)。

## 索引

| 库 | 功能 | 常见使用方 |
| --- | --- | --- |
| harfbuzz | OpenType 文本整形（text shaping） | Pango、Qt、Firefox、Chromium、LibreOffice、OpenJDK |
| freetype | 字体解析与字形光栅化 | Linux 桌面、Android、OpenJDK、各类游戏引擎 |
| giflib | GIF 图片编解码 | OpenJDK、ImageMagick |
| libpng | PNG 图片编解码 | 几乎所有图形软件 |
| jpeg-turbo | JPEG 编解码（libjpeg 的 SIMD 加速实现） | OpenJDK、浏览器、ImageMagick |
| little-cms2 | 色彩管理（ICC profile） | OpenJDK、GIMP、Ghostscript |

## 包名对照

各平台的包名不完全一致，Linux 发行版通常把运行时库和开发头文件拆成两个包，编译其他软件时需要装带 dev / devel 的那个。

| 库 | Homebrew | Debian / Ubuntu（开发包） | Arch | Fedora / RHEL（开发包） |
| --- | --- | --- | --- | --- |
| harfbuzz | `harfbuzz` | `libharfbuzz-dev` | `harfbuzz` | `harfbuzz-devel` |
| freetype | `freetype` | `libfreetype-dev` | `freetype2` | `freetype-devel` |
| giflib | `giflib` | `libgif-dev` | `giflib` | `giflib-devel` |
| libpng | `libpng` | `libpng-dev` | `libpng` | `libpng-devel` |
| jpeg-turbo | `jpeg-turbo` | `libjpeg-dev` | `libjpeg-turbo` | `libjpeg-turbo-devel` |
| little-cms2 | `little-cms2` | `liblcms2-dev` | `lcms2` | `lcms2-devel` |

Arch 和 Homebrew 没有 dev / devel 拆分，头文件和库在同一个包里。

## harfbuzz

[HarfBuzz](https://github.com/harfbuzz/harfbuzz) 是 OpenType 文本整形引擎，许可证 MIT。

### 文本整形是什么

Unicode 文本只是一串字符编号，屏幕上显示的是字形（glyph）。从字符到字形不是一一对应的：

- 连字：`fi` 在字体里可能是一个合并的字形
- 上下文变形：阿拉伯文同一个字母在词首、词中、词尾的字形不同
- 字符重排与组合：天城文（印地语等）的元音符号可能显示在辅音前面，泰文的声调符号叠在字母上方
- 字距调整（kerning）：`AV` 之间的间距比 `AA` 更小

整形（shaping）就是把「字符序列 + 字体」转换成「字形序列 + 每个字形的位置」，HarfBuzz 做的就是这件事。

### 与 FreeType 的分工

| 步骤 | 负责的库 | 说明 |
| --- | --- | --- |
| 读取字体文件、把字形画成位图或轮廓 | FreeType | 光栅化 |
| 决定用哪些字形、放在什么位置 | HarfBuzz | 文本整形 |
| 排版、断行、双向文本 | Pango 等上层库 | 布局 |

两者经常一起出现，HarfBuzz 依赖 FreeType 读取字体数据，所以装 harfbuzz 时通常也会带上 freetype。

### 是不是 OpenJDK 或 macOS 专用的

不是。HarfBuzz 是跨平台的通用库，Linux、macOS、Windows、Android 上都有使用。

OpenJDK 的 Java2D 用它来渲染复杂文字，OpenJDK 源码里自带一份 HarfBuzz，构建时可以选择：

```bash
# Use the bundled copy in the OpenJDK source tree
--with-harfbuzz=bundled

# Use the library installed on the system
--with-harfbuzz=system
```

Homebrew 的 openjdk formula 选的是 `system`，所以 `brew install openjdk` 会依赖并安装 harfbuzz。在 `brew info harfbuzz` 里能看到 `Installed (as dependency)`，`brew uses --installed harfbuzz` 能查到是谁依赖了它。

macOS 本身用 CoreText 做文本整形，系统 App 不需要 HarfBuzz。Homebrew 里的开源软件为了跨平台，才统一使用 HarfBuzz。

### 各平台安装

```bash
# macOS
brew install harfbuzz

# Debian / Ubuntu
sudo apt install libharfbuzz-dev

# Arch Linux
sudo pacman -S harfbuzz

# Fedora
sudo dnf install harfbuzz-devel
```

只是被别的软件依赖时，一般不需要手动安装，包管理器会自动处理。

### 命令行工具

HarfBuzz 自带 `hb-shape`、`hb-view` 等调试工具，可以查看某段文字在某个字体下整形出的字形序列：

```bash
hb-shape /path/to/font.ttf "office"
```

## 相关文章

- [Homebrew (brew)](../macos/brew.md)：不认识的包怎么查
- [FreeType](../cs/freetype.md)
- [font, 字体](../other/font.md)
