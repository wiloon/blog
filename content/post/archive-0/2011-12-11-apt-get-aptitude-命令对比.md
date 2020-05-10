---
title: Apt-get, aptitude 命令对比
author: wiloon
type: post
date: 2011-12-11T03:46:11+00:00
url: /?p=1845
bot_views:
  - 2
views:
  - 3
categories:
  - Linux

---
# <span class="Apple-style-span" style="font-size: 15px;">出自Guoshuang Wiki</span> {#firstHeading}

[http://wiki.guoshuang.com/Apt-get\_%E5%92%8C\_aptitude_%E5%91%BD%E4%BB%A4%E5%AF%B9%E6%AF%94%E5%8F%82%E8%80%83][1]

<div id="bodyContent">
  <div id="contentSub">
  </div>
  
  <table border="1" cellpadding="4">
    <tr>
      <td>
        <strong>Apt-get commands</strong>
      </td>
      
      <td>
        <strong>Aptitude commands</strong>
      </td>
      
      <td>
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get install package
      </td>
      
      <td>
        aptitude install package
      </td>
      
      <td>
        install package 安装软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get install package<code>--</code>reinstall
      </td>
      
      <td>
      </td>
      
      <td>
        reinstall package 重新安装
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get -f install
      </td>
      
      <td>
      </td>
      
      <td>
        force install 强制安装
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get remove package
      </td>
      
      <td>
        aptitude remove package
      </td>
      
      <td>
        remove package 删除软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get remove package<code>--</code>purge
      </td>
      
      <td>
        aptitude purge package
      </td>
      
      <td>
        remove package, include configuration files 删除软件及其配置文件
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get autoremove
      </td>
      
      <td>
      </td>
      
      <td>
        auto remove unused packages 自动删除没用的软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get update
      </td>
      
      <td>
        aptitude update
      </td>
      
      <td>
        update the list of available packages 升级软件更新列表
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get upgrade
      </td>
      
      <td>
        aptitude upgrade
      </td>
      
      <td>
        upgrade packages 升级软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get dist-upgrade
      </td>
      
      <td>
        aptitude dist-upgrade
      </td>
      
      <td>
        upgrade to a new release 升级到下一个发行版
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get build-dep package
      </td>
      
      <td>
      </td>
      
      <td>
        install build dependency 安装编译依赖库
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get source package
      </td>
      
      <td>
      </td>
      
      <td>
        download source 下载源代码
      </td>
    </tr>
    
    <tr>
      <td>
        apt-get clean && apt-get autoclean
      </td>
      
      <td>
        aptitude clean && aptitude autoclean
      </td>
      
      <td>
        remove unused package files 删除没用的软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-cache search package
      </td>
      
      <td>
        aptitude search package
      </td>
      
      <td>
        search packages 在 cache 中搜索软件包
      </td>
    </tr>
    
    <tr>
      <td>
        apt-cache show package
      </td>
      
      <td>
      </td>
      
      <td>
        get more information 显示软件包信息
      </td>
    </tr>
  </table>
</div>

 [1]: http://wiki.guoshuang.com/Apt-get_%E5%92%8C_aptitude_%E5%91%BD%E4%BB%A4%E5%AF%B9%E6%AF%94%E5%8F%82%E8%80%83