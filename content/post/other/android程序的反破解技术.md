---
title: Android程序的反破解技术
author: "-"
date: 2014-03-20T05:56:17+00:00
url: /?p=6410
categories:
  - Uncategorized

tags:
  - reprint
---
## Android程序的反破解技术

<http://blog.csdn.net/viviwen123/article/details/9117589>

逆向Android软件的步骤: 首先是对其进行反编译，然后阅读反汇编代码，如果有必要还会对其进行动态调试，找到突破口后注入或直接修改反汇编代码，最后重新编译软件进行测试。整个过程可分为反编译、静态分析、动态调试、重编译等4个环节。反破解技术也是从这四个方面进行的。

**一、对抗反编译工具** (如ApkTool、BackSmali、dex2jar) ，使其无法进行反编译，或者反编译后无法得到软件正确的反汇编代码。

思路是: 寻找反编译工具在处理apk或dex文件时的缺陷，然后在自己的软件中加以利用。主要方法有:

1. 阅读反编译工具源码。

2. 压力测试。测试大量apk文件，找到反编译工具反编译不了的，分析其特征。

此方法难度较大，而且反编译工具不断升级，方法容易过时，因此不太建议。

二、对抗静态分析。

1. 代码混淆技术: Android2.3的SDK中正式加入了ProGuard代码混淆工具，开发人员可以使用该工具对自己的代码进行混淆。Android2.3以前的项目同样可以使用此工具。

2. NDK保护。

3. 外壳保护。java由于其语言自身特殊性，没有外壳保护这个概念，只能通过混淆方式对其进行保护。外壳保护重点针对使用NDK编写的Native代码，逆向Native本身就已经够困难了，如果添加了外壳保护则更是难上加难，目前已知可用于ARM Linux内核程序的加壳工具只有upx。

三、对抗动态调试。

1. 检测调试器: 动态调试使用调试器来挂钩软件，获取软件运行时的数据，我们可以在软件中加入检测调试器的代码，当检测到软件被调试器连接时，中止软件的运行。

首先，在AndroidManifest.xml文件的Application标签中加入android:debuggable="false"，让程序不可调试，这样，如果别人想调试该程序，就必然会修改它的值，我们在代码中检查它的值来判断程序是否被修改过。代码如下:

      if (0!=(getApplicationInfo().flags&=ApplicationInfo.FLAG_DEBUGGABLE)) {
    
    
                  Log.e("DEBUG", "程序被修改为可调试状态！！！");
    
    
                  android.os.Process.killProcess(android.os.Process.myPid());
    
    
              }

另外，Android SDK中提供了一个方法方便程序员来检测调试器是否已经连接，代码如下:

      android.os.Debug.isDebuggerConnected()

如果方法返回真，说明了调试器已经连接。我们可以随机地在软件中插入这行代码来检测调试器，碰到有调试器连接就果断地结束程序运行。

2. 检测模拟器。

软件发布后会安装到用户的手机中运行，如果有发现软件运行在模拟器中，很显然不合常理，可能是有人试图破解或分析它，这种情况我们必须予以阻止。

模拟器与真实的Android手机有许多差异，我们可以在命令提示符下执行"adb shell getprop"查看并对比它们的属性值，经过对比发现如下几个属性值可以用来判断软件是否运行在模拟器中:

ro.product.model、ro.build.tag、ro.kernel.qemu。编写检测代码如下:

      boolean isRunningInEmualtor() {
    
    
              boolean qemuKernel = false;
    
    
              Process process = null;
    
    
              DataOutputStream os = null;
    
    
              try{
    
    
                  process = Runtime.getRuntime().exec("getprop ro.kernel.qemu");
    
    
                  os = new DataOutputStream(process.getOutputStream());
    
    
                  BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream(),"GBK"));
    
    
                  os.writeBytes("exit\n");
    
    
                  os.flush();
    
    
                  process.waitFor();
    
    
                  qemuKernel = (Integer.valueOf(in.readLine()) == 1);
    
    
                  Log.d("com.droider.checkqemu", "检测到模拟器:" + qemuKernel);
    
    
              } catch (Exception e){
    
    
                  qemuKernel = false;
    
    
                  Log.d("com.droider.checkqemu", "run failed" + e.getMessage());
    
    
              } finally {
    
    
                  try{
    
    
                      if (os != null) {
    
    
                          os.close();
    
    
                      }
    
    
                      process.destroy();
    
    
                  } catch (Exception e) {
    
    
    
    
                  }
    
    
                  Log.d("com.droider.checkqemu", "run finally");
    
    
              }
    
    
              return qemuKernel;
    
    
          }
    
    
    
    
          public static String getProp(Context context, String property) {
    
    
              try {
    
    
                  ClassLoader cl = context.getClassLoader();
    
    
                  Class SystemProperties = cl.loadClass("android.os.SystemProperties");
    
    
                  Method method = SystemProperties.getMethod("get", String.class);
    
    
                  Object[] params = new Object[1];
    
    
                  params[0] = new String(property);
    
    
                  return (String)method.invoke(SystemProperties, params);
    
    
              } catch (Exception e) {
    
    
                  return null;
    
    
              }
    
    
          }

四、防止重编译。

1. 检查签名。每一个软件在发布时都需要开发人员对其进行签名，而签名使用的密钥文件是开发人员所独有的，破解者通常不可能拥有相同的密钥文件，因此，签名成了Andriod软件一种有效的身份标识，如果软件运行时的签名与自己发布时的不同，说明软件被篡改过，这个时候我们就可以让软件中止运行。

获取签名hash值的代码如下:

      public int getSignature(String packageName) {
    
    
              PackageManager pm = this.getPackageManager();
    
    
              PackageInfo pi = null;
    
    
              int sig = 0;
    
    
              try {
    
    
                  pi = pm.getPackageInfo(packageName, PackageManager.GET_SIGNATURES);
    
    
                  Signature[] s = pi.signatures;
    
    
                  sig = s[0].hashCode();
    
    
              } catch (Exception e1) {
    
    
                  sig = 0;
    
    
                  e1.printStackTrace();
    
    
              }
    
    
              return sig;
    
    
          }

可使用Eclipse自带的调试版密钥文件生成的apk文件的hash值,与上面的函数获取的hash比较，可以判断签名是否一致。

2. 校验保护。

重编译Andriod软件的实质是重新编译classes.dex文件，代码经过重新编译后，生成的classes.dex文件的hash值已经改变，我们可以检查程序安装后classes.dex文件的Hash值，来判断软件是否被重打包过。

        private boolean checkCRC() {
    
    
          boolean beModified = false;
    
    
          long crc = Long.parseLong(getString(R.string.crc));
    
    
          ZipFile zf;
    
    
      try {
    
    
          zf = new ZipFile(getApplicationContext().getPackageCodePath());
    
    
          ZipEntry ze = zf.getEntry("classes.dex");
    
    
          Log.d("com.droider.checkcrc", String.valueOf(ze.getCrc()));
    
    
          if (ze.getCrc() == crc) {
    
    
              beModified = true;
    
    
          }
    
    
      } catch (IOException e) {
    
    
          e.printStackTrace();
    
    
          beModified = false;
    
    
      }
    
    
      return beModified;
    
    
        }

本文是阅读《Android软件安全与逆向分析》之【Android程序的反破解技术】一章之后的笔记，想了解更多内容可自行买书~
