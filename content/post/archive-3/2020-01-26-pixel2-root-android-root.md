---
title: pixel2 root, android root
author: wiloon
type: post
date: 2020-01-26T10:16:33+00:00
url: /?p=15417
categories:
  - Uncategorized

---
<blockquote class="wp-embedded-content" data-secret="dymLQPYWmm">
  <p>
    <a href="https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/">Root Android Q on Google Pixel 2, Google Pixel</a>
  </p>
</blockquote>

<iframe title="&#8220;Root Android Q on Google Pixel 2, Google Pixel&#8221; &#8212; Team Android" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://www.teamandroid.com/2019/03/17/root-android-q-beta-google-pixel-2-pixel/embed/#?secret=dymLQPYWmm" data-secret="dymLQPYWmm" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

线刷 android 10

<blockquote class="wp-embedded-content" data-secret="Im4BCxWQUv">
  <p>
    <a href="http://blog.wiloon.com/?p=7296">安卓线刷升级 flash factory image for android device</a>
  </p>
</blockquote>

<iframe title="&#8220;安卓线刷升级 flash factory image for android device&#8221; &#8212; w1100n" class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.wiloon.com/?p=7296&#038;embed=true#?secret=Im4BCxWQUv" data-secret="Im4BCxWQUv" width="600" height="338" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

Enable USB Debugging mode
   
Download MagiskManager apk 并安装 到手机
  
从第一步线刷升级用的镜像文件 里解压出boot.img, 传到手机 上的download目录
  
打开magisk mamanger, 点击 &#8220;未安装 Magisk&#8221; 后面的安装按钮， 在弹出的菜单中选择 “选择并修补一个文件 ”， 然后 选择boot.img。
  
把打好补丁的boot.img传到电脑 上 ， 打补丁之后的boot.img的名字 应该 是magisk_patched.img
  
执行 adb reboot bootloader，到bootloader
  
刷入打好补丁的 boot.img

```bashfastboot flash boot patched_boot.img
fastboot reboot
```

重启后系统已经root成功了。