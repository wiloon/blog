---
title: Android App签名
author: wiloon
type: post
date: 2014-12-30T09:09:43+00:00
url: /?p=7159
categories:
  - Uncategorized

---
**1.签名的意义**
  
为了保证每个应用程序开发商合法ID，防止部分开放商可能通过使用相同的Package Name来混淆替换已经安装的程序，我们需要对我们发布的APK文件进行唯一签名，保证我们每次发布的版本的一致性(如自动更新不会因为版本不一致而无法安装)。

**2.签名的步骤**
  
a.创建key
  
b.使用步骤a中产生的key对apk签名

**3.具体操作**

_**方法一： 命令行下对apk签名（原理）**_
  
创建key，需要用到keytool.exe (位于jdk1.6.0\_24\jre\bin目录下)，使用产生的key对apk签名用到的是jarsigner.exe (位于jdk1.6.0\_24\bin目录下)，把上两个软件所在的目录添加到环境变量path后，打开cmd输入

<div class="cnblogs_Highlighter">
  
    <div id="highlighter_790413" class="syntaxhighlighter nogutter  fsharp">
      <table border="0" cellspacing="0" cellpadding="0">
        <tr>
          <td class="code">
            <div class="container">
              <div class="line number1 index0 alt2">
                <code class="fsharp plain">D:\>keytool -genkey -alias demo.keystore -keyalg RSA -validity 40000 -keystore demo.keystore</code>
              
              
              <div class="line number2 index1 alt1">
                <code class="fsharp plain">/*说明：-genkey 产生密钥</code>
              
              
              <div class="line number3 index2 alt2">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-alias demo.keystore 别名 demo.keystore</code>
              
              
              <div class="line number4 index3 alt1">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-keyalg RSA 使用RSA算法对签名加密</code>
              
              
              <div class="line number5 index4 alt2">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-validity 40000 有效期限4000天</code>
              
              
              <div class="line number6 index5 alt1">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-keystore demo.keystore */</code>
              
              
              <div class="line number7 index6 alt2">
                <code class="fsharp plain">D:\>jarsigner -verbose -keystore demo.keystore -signedjar demo_signed.apk demo.apk demo.keystore</code>
              
              
              <div class="line number8 index7 alt1">
                <code class="fsharp plain">/*说明：-verbose 输出签名的详细信息</code>
              
              
              <div class="line number9 index8 alt2">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-keystore  demo.keystore 密钥库位置</code>
              
              
              <div class="line number10 index9 alt1">
                <code class="fsharp spaces">       </code><code class="fsharp plain">-signedjar demor_signed.apk demo.apk demo.keystore 正式签名，三个参数中依次为签名后产生的文件demo_signed，要签名的文件demo.apk和密钥库demo.keystore.*/</code>
              
            
          </td>
        </tr>
      </table>
    
  


注意事项：android工程的bin目录下的demo.apk默认是已经使用debug用户签名的，所以不能使用上述步骤对此文件再次签名。正确步骤应该是:在工程点击右键->Anroid Tools-Export Unsigned Application Package导出的apk采用上述步骤签名。