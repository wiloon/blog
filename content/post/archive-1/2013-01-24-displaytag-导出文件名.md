---
title: displaytag 导出文件名
author: w1100n
type: post
date: 2013-01-24T07:07:57+00:00
url: /?p=5071
categories:
  - Java

---
http://magicgod.iteye.com/blog/173225

displaytag还算是比较好的，可以分页（可以配合hibernate分页，显示行数有个小bug，不过已经提交bug了，据说下个版本改），可以任意调整显示内容，可以输出很多种格式。

不过缺省情况下输出的文件名不对，后缀名不按类型来，幸好可以配置displaytag.properties

一般来说是放在WEB-INF/classes/下的。

配一下导出文件名

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://magicgod.iteye.com/images/icon_star.png" /></a>
  
  
  <ol start="1">
    <li>
      export.pdf.filename=export.pdf
    </li>
    <li>
      export.csv.filename=export.csv
    </li>
    <li>
      export.excel.filename=export.xsl
    </li>
    <li>
      export.xml.filename=export.xml
    </li>
  </ol>

但可惜的是不能用动态文件名，看了一下源码是这样写的：

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://magicgod.iteye.com/images/icon_star.png" /></a>
  
  
  <ol start="1">
    <li>
      public String getExportFileName(MediaTypeEnum exportType)
    </li>
    <li>
      {
    </li>
    <li>
          return getProperty(PROPERTY_EXPORT_PREFIX + SEP + exportType.getName() + SEP + EXPORTPROPERTY_STRING_FILENAME);
    </li>
    <li>
      }
    </li>
  </ol>

没戏了，根据导出类型从属性里取一个静态的文件名。

是这样应用的：

<div id="">
  
    
      Java代码  <a title="收藏这段代码"><img alt="收藏代码" src="http://magicgod.iteye.com/images/icon_star.png" /></a>
  
  
  <ol start="1">
    <li>
      String filename = properties.getExportFileName(this.currentMediaType);
    </li>
    <li>
    </li>
    <li>
      if (StringUtils.isNotEmpty(filename))
    </li>
    <li>
      {
    </li>
    <li>
          response.setHeader("Content-Disposition", //$NON-NLS-1$
    </li>
    <li>
              "attachment; filename="" + filename + """); //$NON-NLS-1$ //$NON-NLS-2$
    </li>
    <li>
      }
    </li>
  </ol>

彻底没指望了，直接拿出来就放在header里了。算了，凑和吧。