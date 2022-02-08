---
title: adb Shell root 权限
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6891
categories:
  - Uncategorized

tags:
  - reprint
---
## adb Shell root 权限
http://www.cnblogs.com/blues_/p/3582097.html

转adb Shell root 权限

永久root带文件

因为开发需要，我经常会用到adb这个工具(Android Debug Bridge)，我们都知道adb shell默认是没有root权限的，修改系统文件就很不方便了，adb push一个文件就提示Permission Denied。删除system下的文件也没有权限。其实有两种方法可以获取adb shell的root权限，这两种方法的前提都是手机已经root。 1、用su可以提权，直接执行su就会看到用户命令提示符由"$"变成了"#"，如果手机没有root，会提示su: Permission Denied。这个文件不是每个手机都有的，可以百度。 解压后把su放在adb同一目录下，执行: 

adb push su /system/bin/adb shell chmod4755/system/bin/su

如果提示Read-only filesystem，那么就要重新挂载一下/system，把只读挂载成可读写，只有手机root了才能运行: 

mount -o remount,rw/dev/block/mtdblock0/system /

再运行su就能让adb shell获取root权限了。 2、可以修改根目录下的default.prop提权:  根目录默认是不允许修改的，执行

mount -o remount,rw rootfs/

用vi打开default.prop，找到ro.secure，修改为ro.secure=0，保存后重启，再adb shell一下，就会有root权限了。 方法: 

修改./default.prop

把ro.secure设为0，persist.service.adb.enable设为1，adbd进程就会以root用户的身份启动。

其实两篇文章大体效果不同，这个是完全破除限制，下文只是部分 至于文中所提到的su文件，是指被修改过的，无任何验证的，这样安全性大大降低，推荐完整root前，先备份原su文件。


原理: 

可以看一下Android系统根目录下的/init.rc的片段: 

... ...

# adbd is controlled by the persist.service.adb.enable system property

service adbd /sbin/adbd

disabled

# adbd on at boot in emulator

on property:ro.kernel.qemu=1

start adbd

on property:persist.service.adb.enable=1

start adbd

on property:persist.service.adb.enable=0

stop adbd

... ...

这里定义了一个触发器，只要persist.service.adb.enable值被置为1，就会启动/sbin/adbd。


在build目录下搜索一下，发现了main.mk中有这样的代码片段

## user/userdebug ##


user_variant := $(filter userdebug user,$(TARGET_BUILD_VARIANT))

enable_target_debugging := true

ifneq (,$(user_variant))

# Target is secure in user builds.

ADDITIONAL_DEFAULT_PROPERTIES += ro.secure=1


tags_to_install := user

ifeq ($(user_variant),userdebug)

# Pick up some extra useful tools

tags_to_install += debug

else

# Disable debugging in plain user builds.

enable_target_debugging :=

endif


# TODO: Always set WITH_DEXPREOPT (for user builds) once it works on OSX.

# Also, remove the corresponding block in config/product_config.make.

ifeq ($(HOST_OS)-$(WITH_DEXPREOPT_buildbot),linux-true)

WITH_DEXPREOPT := true

endif


# Disallow mock locations by default for user builds

ADDITIONAL_DEFAULT_PROPERTIES += ro.allow.mock.location=0


else # !user_variant

# Turn on checkjni for non-user builds.

ADDITIONAL_BUILD_PROPERTIES += ro.kernel.android.checkjni=1

# Set device insecure for non-user builds.

ADDITIONAL_DEFAULT_PROPERTIES += ro.secure=0

# Allow mock locations by default for non user builds

ADDITIONAL_DEFAULT_PROPERTIES += ro.allow.mock.location=1

endif # !user_variant


ifeq (true,$(strip $(enable_target_debugging)))

# Target is more debuggable and adbd is on by default

ADDITIONAL_DEFAULT_PROPERTIES += ro.debuggable=1 persist.service.adb.enable=1

# Include the debugging/testing OTA keys in this build.

INCLUDE_TEST_OTA_KEYS := true

else # !enable_target_debugging

# Target is less debuggable and adbd is off by default

ADDITIONAL_DEFAULT_PROPERTIES += ro.debuggable=0 persist.service.adb.enable=0

endif # !enable_target_debugging

这段代码我大致解释一下: 

主要通过判断当前的编译模式来给几个属性赋予不同的值，然后把属性存储在ADDITIONAL_DEFAULT_PROPERTIES这个变量中，这个变量在后面是要写到根目录下的/default.prop中去，在系统启动时被属性服务加载的。也就是说我们在/default.prop中看到的几个属性的值是在这里设置的。

只看两个属性ro.secure，persist.service.adb.enable。当前是user模式的话，编译系统会把ro.secure置为1，把persist.service.adb.enable置为0.也就是说，用user模式编译出来的系统运行在安全模式下，adbd默认关闭。即使通过设置属性的方式打开，adbd进程的用户也是shell，不具有root权限。这样，普通用户或者开发者拿到一个机器后，通过PC运行adb shell时，是以shell用户登录机器的。

好了，现在把ro.secure置为0，再重新编译，只要设置属性persist.service.adb.enable的值为1，adbd进程就会以root用户的身份启动。