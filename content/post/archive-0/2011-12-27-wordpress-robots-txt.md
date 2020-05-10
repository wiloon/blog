---
title: WordPress, robots.txt
author: wiloon
type: post
date: 2011-12-27T03:11:09+00:00
url: /?p=2032
categories:
  - Wordpress

---
<div>
  <div>
    <div>
      <p>
        我们都希望搜索引擎多多收录我们的页面，收录越多越好，但是会存在另一个问题，同一个页面收录多次的话会降低页面的权重，在搜索结果中排名位置不理想。对于所有网站来说，可以使用robots.txt文件来限制搜索引擎的收录情况，对于WordPress来说这也不例外.
      </p>
    </div>
  </div>
</div>

<div>
  <p>
    重复收录的坏处形象地说：如果一个页面的权重是1，那么如果你收录的内容里有重复的，那么两个页面会变成0.5（仅仅是例子，现实中可能不会这样准确，但是原理差不多）甚至更低，权重低就意味着在搜索结果中出现的位置靠后。所以我们必须剔除重复的链接。
  </p>
  
  <h2>
    为WordPress创建robots.txt
  </h2>
  
  <p>
    如果你的WordPress空间里没有robots.txt文章可以新建一个，编码格式设置为utf-8（需要注意的是，WordPress默认情况下会自动生成一个robots.txt，不过这个文件是虚拟的）。
  </p>
  
  <p>
    在参考了网上几个robots.txt的例子之后，我结合自己的实际情况写了下面一个：
  </p>
  
  <blockquote>
    <p>
      User-agent: *<br /> Disallow: /cgi-bin<br /> Disallow: /wp-*<br /> Allow: /wp-content/uploads/<br /> Disallow: /feed/<br /> Disallow: /comments/feed<br /> Disallow: /trackback<br /> Disallow:/tag/<br /> Disallow:/page/*<br /> Disallow: /comments<br /> Disallow: /category/*/page/*<br /> Disallow: /category/*<br /> Disallow:/duam/<br /> Disallow:/date/<br /> Disallow: /*.php$<br /> Disallow: /*.inc$<br /> Disallow: /*.js$<br /> Disallow: /*.css$<br /> Disallow: /*?*<br /> Disallow: /*?<br /> Disallow: /?s=<br /> Sitemap: http://dudo.org/sitemap.xml<br /> Sitemap: http://dudo.org/sitemap.xml.gz
    </p>
  </blockquote>
  
  <p>
    简单说一下，WordPress目录下，除了保存的附件的/wp-content/uploads/目录外，其他实体目录都不允许访问，而虚拟目录/page/、/data/、/category/等会造成重复收录，同时我们还要禁止所有php、js、css等文件的收录，因为这些文件和我们网站的内容没有任何关系；此外，/*?*、/*?等是禁止所有带参数的链接（<strong>因为我的页面链接都是目录形式的，如果你的是使用参数形式的这里设置要谨慎。</strong>）最后两行是告诉搜索引擎你的网站地图，便于收录（其实只要一个就行了，而且要安装了Google XML sitemap插件）。
  </p>
  
  <h2>
    测试WordPress中的Robots.txt
  </h2>
  
  <p>
    在WordPress中创建好robots.txt后，你可以通过Google站长管理工具来测试和管理你的robots.txt文件，听说百度也要出百度站长管理工具了，将来也可以通过它来管理，其实我们网站搜索引擎的流量也主要来自这两个。
  </p>
  
  <p>
    在Google站长管理工具中“网站配置->抓取工具权限”下，你会看到Google已经抓取并显示了wordpress下的robots.txt里面的内容，我们可以在下面的条件测试中依次输入不同的网址形式来看结果（<strong>这个过程也有利于防止出现因为robots.txt规则太多而出现的抓取错误</strong>）.
  </p>
  
  <p>
    测试结果中我们可以看到哪条规则对测试的链接方式起作用，同时我们也可以看到哪些链接形式是允许的，哪些是禁止的，经过多次测试我们可以达到最佳robots.txt效果。
  </p>
  
  <p>
    <a href="http://www.robotstxt.org/">http://www.robotstxt.org/</a>
  </p>
  
  <p>
    <a href="http://www.robotstxt.org/orig.html">http://www.robotstxt.org/orig.html</a>
  </p>
  
  <p>
    <a href="http://support.google.com/webmasters/bin/answer.py?hl=zh-Hans&answer=156449">http://support.google.com/webmasters/bin/answer.py?hl=zh-Hans&answer=156449</a>
  </p>
</div>