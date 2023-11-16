---
title: HTML5 中 div section article 的区别
author: "-"
date: 2012-02-19T12:21:06+00:00
url: /?p=2374
categories:
  - Web
tags:
  - HTML

---
## HTML5 中 div section article 的区别
## div {#toc_1.1}

HTML Spec: "The div element has no special meaning at all."

这个标签是我们见得最多、用得最多的一个标签。本身没有任何语义，用作布局以及样式化或脚本的钩子(hook)。

## section {#toc_1.2}

HTML Spec: "The section element represents a generic section of a document or application. A section, in this context, is a thematic grouping of content, typically with a heading."

与 div 的无语义相对，简单地说 section 就是带有语义的 div 了，但是千万不要觉得真得这么简单。section 表示一段专题性的内容，一般会带有标题。看到这里，我们也许会想到，那么一篇博客文章，或者一条单独的评论岂不是正好可以用 section 吗？接着看: 

"Authors are encouraged to use the article element instead of the section element when it would make sense to syndicate the contents of the elemen."

当元素内容聚合起来更加言之有物时，应该使用 article 来替换 section 。

那么，section 应该什么时候用呢？再接着看: 

"Examples of sections would be chapters, the various tabbed pages in a tabbed dialog box, or the numbered sections of a thesis. A Web site's home page could be split into sections for an introduction, news items, and contact information."

section 应用的典型场景有文章的章节、标签对话框中的标签页、或者论文中有编号的部分。一个网站的主页可以分成简介、新闻和联系信息等几部分。其实我对这里传达信息很感兴趣，因为感觉 section 和下面要介绍的 artilce 更加适用于模块化应用，这个话题以后会出篇专门的文章来讨论，这里暂时略过。

要注意，W3C 还警告说: 

"The section element is not a generic container element. When an element is needed for styling purposes or as a convenience for scripting, authors are encouraged to use the div element instead. A general rule is that the section element is appropriate only if the element's contents would be listed explicitly in the document's outline."

section 不仅仅是一个普通的容器标签。当一个标签只是为了样式化或者方便脚本使用时，应该使用 div 。一般来说，当元素内容明确地出现在文档大纲中时，section 就是适用的。


 <hgroup>
  Apples
  Tasty, delicious fruit!
 </hgroup>
 The apple is the pomaceous fruit of the apple tree.
 <section>
  Red Delicious
  These bright red apples are the most common found in many
  supermarkets.
 </section>
 <section>
  Granny Smith
  These juicy, green apples make a great filling for
  apple pies.
 </section>
</article>

## article {#toc_1.3}

HTML Spec: "The article element represents a self-contained composition in a document, page, application, or site and that is, in principle, independently distributable or reusable, e.g. in syndication."

article 是一个特殊的 section 标签，它比 section 具有更明确的语义, 它代表一个独立的、完整的相关内容块。一般来说， article 会有标题部分(通常包含在 header 内)，有时也会 包含 footer 。虽然 section 也是带有主题性的一块内容，但是无论从结构上还是内容上来说，article 本身就是独立的、完整的。

HTML Spec 中接着又列举了一些 article 适用的场景。 "This could be a forum post, a magazine or newspaper article, a blog entry, a user-submitted comment, an interactive widget or gadget, or any other independent item of content."

当 article 内嵌 article 时，原则上来说，内部的 article 的内容是和外层的 article 内容是相关的。例如，一篇博客文章中，包含用户提交的评论的 article 就应该潜逃在包含博客文章 article 之中。

问题是怎么才算"完整的独立内容"？有个最简单的判断方法是看这段内容在 RSS feed 中是不是完整的。看这段内容脱离了所在的语境，是否还是完整的、独立的。

例子: 


 
  The Very First Rule of Life
  <time pubdate datetime="2009-10-09T14:28-08:00"></time>
 
 If there's a microphone anywhere near you, assume it's hot and
 sending whatever you're saying to the world. Seriously.
 ...
 <footer>
  Show comments...
 </footer>
</article>

 
  The Very First Rule of Life
  <time pubdate datetime="2009-10-09T14:28-08:00"></time>
 
 If there's a microphone anywhere near you, assume it's hot and
 sending whatever you're saying to the world. Seriously.
 ...
 <section>
  Comments
  
   <footer>
    Posted by: George Washington
    <time pubdate datetime="2009-10-10T19:10-08:00"></time>
   </footer>
   Yeah! Especially when talking about your lobbyist friends!
  </article>
  
   <footer>
    Posted by: George Hammond
    <time pubdate datetime="2009-10-10T19:15-08:00"></time>
   </footer>
   Hey, you have the same first name as me.
  </article>
 </section>
</article>

## 总结 {#toc_1.4}

div section article ，语义是从无到有，逐渐增强的。div 无任何语义，仅仅用作样式化或者脚本化的钩子(hook)，对于一段主题性的内容，则就适用 section，而假如这段内容可以脱离上下文，作为完整的独立存在的一段内容，则就适用 article。原则上来说，能使用 article 的时候，也是可以使用 section 的，但是实际上，假如使用 article 更合适，那么就不要使用 section 。nav 和 aside 的使用也是如此，这两个标签也是特殊的 section，在使用 nav 和 aside 更合适的情况下，也不要使用 section 了。

对于 div 和 section、 article 以及其他标签的区分比较简单。对于 section 和 article 的区分乍看比较难，其实重点就是看看这段内容脱离了整体是不是还能作为一个完整的、独立的内容而存在，这里面的重点又在完整身上。因为其实说起来 section 包含的内容也能算作独立的一块，但是它只能算是组成整体的一部分，article 才是一个完整的整体。

因为其实有些时候每个人都有自己的看法，所以难免有难于决断的时候，怎么办？

在 [HTML5 设计原理][1] 中，有一条是专门用来解决类似情况的: 

**最终用户优先(Priority of Constituencies)**

"In case of conflict, consider users over authors over implementors over specifiers over theoretical purity." 一旦遇到冲突，最终用户优先，其次是作者，其次是实现者，其次标准制定者，最后才是理论上的完满。

推荐各位多读几遍 [HTML5 设计原理][1]，这才是纷繁世界背后的最终奥义。

http://gaowhen.com/

[http://www.qianduan.net/html5-differences-in-the-div-section-article.html](http://www.qianduan.net/html5-differences-in-the-div-section-article.html)

 [1]: http://www.cn-cuckoo.com/2010/10/21/the-design-of-html5-2151.html