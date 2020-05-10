---
title: maven cmd utf8 error
author: wiloon
type: post
date: 2014-12-30T05:54:51+00:00
url: /?p=7153
categories:
  - Uncategorized
tags:
  - Maven

---
unmappable character for encoding GBK

&nbsp;

<pre class="default prettyprint prettyprinted"><code>&lt;span class="tag">&lt;properties&gt;&lt;/span>
    &lt;span class="tag">&lt;project.build.sourceEncoding&gt;&lt;/span>&lt;span class="pln">UTF-8&lt;/span>&lt;span class="tag">&lt;/project.build.sourceEncoding&gt;&lt;/span>
    &lt;span class="tag">&lt;project.reporting.outputEncoding&gt;&lt;/span>&lt;span class="pln">UTF-8&lt;/span>&lt;span class="tag">&lt;/project.reporting.outputEncoding&gt;&lt;/span>
&lt;span class="tag">&lt;/properties&gt;&lt;/span></code></pre>

&nbsp;

http://stackoverflow.com/questions/3017695/how-to-configure-encoding-in-maven